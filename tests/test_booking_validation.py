import unittest
from datetime import datetime

from medilink import MediLinkService


class TestBookingValidation(unittest.TestCase):

    def setUp(self):
        self.service = MediLinkService()
        self.service.add_slot(101, "medical", datetime(2026, 11, 5, 10, 0))

    def test_successful_booking(self):
        self.service.book_appointment(1, 101)

        self.assertIn(1, self.service.appointments)
        self.assertTrue(self.service.slots[101].booked)

    def test_duplicate_appointment_id_raises_value_error(self):
        self.service.book_appointment(1, 101)

        with self.assertRaises(ValueError):
            self.service.book_appointment(1, 101)

    def test_booking_nonexistent_slot_raises_value_error(self):
        with self.assertRaises(KeyError):
            self.service.book_appointment(2, 999)


if __name__ == "__main__":
    unittest.main()
