import unittest
from datetime import datetime

from medilink import MediLinkService


class TestDoubleBooking(unittest.TestCase):

    def setUp(self):
        self.service = MediLinkService()
        self.service.add_slot(101, "medical", datetime(2026, 11, 5, 10, 0))

    def test_booked_slot_rejects_second_appointment(self):
        self.service.book_appointment(1, 101)

        with self.assertRaisesRegex(ValueError, "Appointment slot unavailable"):
            self.service.book_appointment(2, 101)

        self.assertEqual(self.service.appointments[1].status, "booked")
        self.assertNotIn(2, self.service.appointments)
        self.assertTrue(self.service.slots[101].booked)

    def test_repeated_cancellation_does_not_release_new_booking(self):
        self.service.book_appointment(1, 101)
        self.service.cancel_appointment(1)

        self.service.book_appointment(2, 101)
        self.service.cancel_appointment(1)

        self.assertEqual(self.service.appointments[2].status, "booked")
        self.assertTrue(self.service.slots[101].booked)


if __name__ == "__main__":
    unittest.main()
