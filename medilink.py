from dataclasses import dataclass
from datetime import datetime


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
        slot = self.slots[slot_id]

        if slot.booked:
            raise ValueError("Appointment slot unavailable")

        slot.booked = True
        self.appointments[appointment_id] = Appointment(
            appointment_id, slot_id
        )
        self.reminder_queue.add(appointment_id)

    def cancel_appointment(self, appointment_id):
        appointment = self.appointments[appointment_id]

        appointment.status = "cancelled"
        self.slots[appointment.slot_id].booked = False

        # Remove pending reminders for cancelled appointments
        self.reminder_queue.discard(appointment_id)

    def send_reminders(self):
        sent = []

        for appointment_id in sorted(self.reminder_queue):
            appointment = self.appointments[appointment_id]

            # Check the latest status before sending
            if appointment.status == "booked":
                sent.append(appointment_id)

        self.reminder_queue.clear()
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

