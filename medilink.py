from dataclasses import dataclass
from datetime import datetime
import json
import logging
import sys


logger = logging.getLogger("medilink")
logger.addHandler(logging.NullHandler())


class JsonLogFormatter(logging.Formatter):
    def format(self, record):
        entry = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if hasattr(record, "event"):
            entry["event"] = record.event
        for field in ("appointment_id", "slot_id", "error_type", "error"):
            if hasattr(record, field):
                entry[field] = getattr(record, field)
        return json.dumps(entry, sort_keys=True)


def configure_logging(stream=None, level=logging.INFO):
    """Configure application logs for a command-line or service entry point."""
    handler = logging.StreamHandler(stream or sys.stderr)
    handler.setFormatter(JsonLogFormatter())
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False


@dataclass
class AppointmentSlot:
    id: int
    clinic_type: str
    starts_at: datetime
    booked: bool = False


@dataclass
class Appointment:
    id: int
    slot_id: int
    status: str = "booked"


class MediLinkService:
    def __init__(self):
        self.slots = {}
        self.appointments = {}
        self.reminder_queue = set()

    def add_slot(self, slot_id, clinic_type, starts_at):
        self.slots[slot_id] = AppointmentSlot(
            slot_id, clinic_type, starts_at
        )

    def book_appointment(self, appointment_id, slot_id):
        try:
            if appointment_id in self.appointments:
                raise ValueError("Appointment already exists")

            if slot_id not in self.slots:
                raise ValueError("Appointment slot not found")

            slot = self.slots[slot_id]

            if slot.booked:
                raise ValueError("Appointment slot unavailable")

            slot.booked = True
            self.appointments[appointment_id] = Appointment(
                appointment_id, slot_id
            )
            self.reminder_queue.add(appointment_id)
        except (KeyError, ValueError) as error:
            logger.error(
                "appointment booking failed",
                extra={
                    "event": "appointment_booking_failed",
                    "appointment_id": appointment_id,
                    "slot_id": slot_id,
                    "error_type": type(error).__name__,
                    "error": str(error),
                },
            )
            raise

        logger.info(
            "appointment booked",
            extra={
                "event": "appointment_booked",
                "appointment_id": appointment_id,
                "slot_id": slot_id,
            },
        )

    def cancel_appointment(self, appointment_id):
        try:
            appointment = self.appointments[appointment_id]

            if appointment.status == "cancelled":
                return

            appointment.status = "cancelled"
            self.slots[appointment.slot_id].booked = False

            # Remove pending reminders for cancelled appointments
            self.reminder_queue.discard(appointment_id)
        except (KeyError, ValueError) as error:
            logger.error(
                "appointment cancellation failed",
                extra={
                    "event": "appointment_cancellation_failed",
                    "appointment_id": appointment_id,
                    "error_type": type(error).__name__,
                    "error": str(error),
                },
            )
            raise

        logger.info(
            "appointment cancelled",
            extra={
                "event": "appointment_cancelled",
                "appointment_id": appointment_id,
            },
        )

    def send_reminders(self):
        sent = []

        for appointment_id in sorted(self.reminder_queue):
            try:
                appointment = self.appointments[appointment_id]

                # Check the latest status before sending
                if appointment.status == "booked":
                    sent.append(appointment_id)
            except (KeyError, ValueError) as error:
                logger.error(
                    "appointment reminder failed",
                    extra={
                        "event": "appointment_reminder_failed",
                        "appointment_id": appointment_id,
                        "error_type": type(error).__name__,
                        "error": str(error),
                    },
                )
                raise

        self.reminder_queue.clear()
        logger.info(
            "appointment reminders processed",
            extra={
                "event": "appointment_reminders_processed",
            },
        )
        return sent

    def search_available_appointments(self, appointment_date=None, clinic_type=None):
        results = []

        for slot in self.slots.values():

            # Skip already booked appointments
            if slot.booked:
                continue

            # Filter by date
            if appointment_date is not None:
                if slot.starts_at.date() != appointment_date:
                    continue

            # Filter by clinic type
            if clinic_type is not None:
                if slot.clinic_type.lower() != clinic_type.lower():
                    continue

            results.append(slot)

        # Sort appointments by date and time
        results.sort(key=lambda slot: slot.starts_at)

        return results

    def reschedule_appointment(self, appointment_id, new_slot_id):

        if appointment_id not in self.appointments:
            raise ValueError("Appointment not found")

        appointment = self.appointments[appointment_id]

        if appointment.status != "booked":
            raise ValueError("Cannot reschedule a cancelled appointment")

        if new_slot_id not in self.slots:
            raise ValueError("Appointment slot not found")

        old_slot_id = appointment.slot_id

        if old_slot_id == new_slot_id:
            raise ValueError("Please select a different time slot")

        new_slot = self.slots[new_slot_id]

        if new_slot.booked:
            raise ValueError("Appointment slot unavailable")

        # Release old appointment slot
        self.slots[old_slot_id].booked = False

        # Reserve new appointment slot
        new_slot.booked = True

        # Update appointment
        appointment.slot_id = new_slot_id

        # Ensure reminder is scheduled
        self.reminder_queue.add(appointment_id)

        return {
            "appointment_id": appointment_id,
            "old_slot_id": old_slot_id,
            "new_slot_id": new_slot_id,
            "message": "Appointment rescheduled successfully"
        }
