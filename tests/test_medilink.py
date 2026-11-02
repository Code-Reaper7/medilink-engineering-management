
import unittest
from datetime import datetime
from medilink import MediLinkService


class TestReminders(unittest.TestCase):

    def setUp(self):
        self.service = MediLinkService()
        self.service.add_slot(
            101, "medical", datetime(2026, 11, 5, 10, 0)
        )
        self.service.book_appointment(1, 101)

    def test_active_appointment_receives_reminder(self):
        self.assertEqual(
            self.service.send_reminders(), [1]
        )

    def test_cancelled_appointment_receives_no_reminder(self):
        self.service.cancel_appointment(1)

        self.assertEqual(
            self.service.send_reminders(), []
        )

    def test_stale_queued_reminder_is_not_sent(self):
        self.service.cancel_appointment(1)

        # Simulate a reminder still sitting in the queue
        self.service.reminder_queue.add(1)

        self.assertEqual(
            self.service.send_reminders(), []
        )

    def test_cancellation_releases_slot(self):
        self.service.cancel_appointment(1)

        self.assertFalse(self.service.slots[101].booked)


if __name__ == "__main__":
    unittest.main()
