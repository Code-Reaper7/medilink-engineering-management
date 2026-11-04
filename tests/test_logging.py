import json
import logging
import unittest
from datetime import datetime
from io import StringIO

from medilink import MediLinkService, configure_logging


class TestAppointmentLogging(unittest.TestCase):

    def setUp(self):
        self.output = StringIO()
        configure_logging(self.output)
        self.service = MediLinkService()
        self.service.add_slot(
            101, "medical", datetime(2026, 11, 5, 10, 0)
        )

    def tearDown(self):
        logging.getLogger("medilink").handlers.clear()
        logging.getLogger("medilink").addHandler(logging.NullHandler())

    def test_booking_failure_logs_error_without_patient_data(self):
        with self.assertRaises(ValueError):
            self.service.book_appointment(1, 999)

        entry = json.loads(self.output.getvalue())
        self.assertEqual(entry["event"], "appointment_booking_failed")
        self.assertEqual(entry["level"], "ERROR")
        self.assertEqual(entry["slot_id"], 999)
        self.assertTrue(entry["timestamp"])

    def test_cancellation_failure_logs_error(self):
        with self.assertRaises(KeyError):
            self.service.cancel_appointment(404)

        entry = json.loads(self.output.getvalue())
        self.assertEqual(entry["event"], "appointment_cancellation_failed")
        self.assertEqual(entry["error_type"], "KeyError")

    def test_reminder_failure_logs_error(self):
        self.service.reminder_queue.add(404)

        with self.assertRaises(KeyError):
            self.service.send_reminders()

        entry = json.loads(self.output.getvalue())
        self.assertEqual(entry["event"], "appointment_reminder_failed")
        self.assertEqual(entry["appointment_id"], 404)

    def test_successful_booking_and_cancellation_are_logged(self):
        self.service.book_appointment(1, 101)
        self.service.cancel_appointment(1)

        entries = [
            json.loads(line) for line in self.output.getvalue().splitlines()
        ]
        self.assertEqual(
            [entry["event"] for entry in entries],
            ["appointment_booked", "appointment_cancelled"],
        )


if __name__ == "__main__":
    unittest.main()
