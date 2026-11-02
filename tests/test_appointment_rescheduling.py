
import unittest
from datetime import datetime, date
from medilink import MediLinkService


class TestAppointmentRescheduling(unittest.TestCase):

    def setUp(self):
        self.service = MediLinkService()

        self.service.add_slot(
            101, "medical", datetime(2026, 11, 5, 10, 0)
        )

        self.service.add_slot(
            102, "medical", datetime(2026, 11, 6, 14, 0)
        )

        self.service.add_slot(
            103, "dental", datetime(2026, 11, 6, 11, 0)
        )

        self.service.book_appointment(1, 101)

    def test_successful_rescheduling(self):
        result = self.service.reschedule_appointment(1, 102)

        self.assertEqual(
            self.service.appointments[1].slot_id, 102
        )
        self.assertEqual(
            result["message"],
            "Appointment rescheduled successfully"
        )

    def test_original_slot_becomes_available(self):
        self.service.reschedule_appointment(1, 102)

        self.assertFalse(self.service.slots[101].booked)
        self.assertTrue(self.service.slots[102].booked)

    def test_prevent_double_booking(self):
        self.service.book_appointment(2, 102)

        with self.assertRaises(ValueError):
            self.service.reschedule_appointment(1, 102)

        self.assertEqual(
            self.service.appointments[1].slot_id, 101
        )
        self.assertTrue(self.service.slots[101].booked)

    def test_cancelled_appointment_cannot_reschedule(self):
        self.service.cancel_appointment(1)

        with self.assertRaises(ValueError):
            self.service.reschedule_appointment(1, 102)

    def test_nonexistent_appointment(self):
        with self.assertRaises(ValueError):
            self.service.reschedule_appointment(999, 102)

    def test_nonexistent_slot(self):
        with self.assertRaises(ValueError):
            self.service.reschedule_appointment(1, 999)

    def test_same_slot_not_allowed(self):
        with self.assertRaises(ValueError):
            self.service.reschedule_appointment(1, 101)

    def test_available_alternative_slots(self):
        results = self.service.search_available_appointments(
            appointment_date=date(2026, 11, 6),
            clinic_type="medical"
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, 102)


if __name__ == "__main__":
    unittest.main()
