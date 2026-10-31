
import unittest
from datetime import datetime, date
from medilink import MediLinkService


class TestAppointmentSearch(unittest.TestCase):

    def setUp(self):
        self.service = MediLinkService()

        self.service.add_slot(
            101, "medical", datetime(2026, 11, 5, 10, 0)
        )

        self.service.add_slot(
            102, "dental", datetime(2026, 11, 5, 11, 0)
        )

        self.service.add_slot(
            103, "medical", datetime(2026, 11, 6, 9, 0)
        )

        self.service.add_slot(
            104, "dental", datetime(2026, 11, 6, 14, 0)
        )

        # Book slot 104 so it is no longer available
        self.service.book_appointment(1, 104)

    def test_show_all_available_appointments(self):
        results = self.service.search_available_appointments()
        self.assertEqual(len(results), 3)

    def test_filter_by_date(self):
        results = self.service.search_available_appointments(
            appointment_date=date(2026, 11, 5)
        )
        self.assertEqual(len(results), 2)

    def test_filter_by_clinic_type(self):
        results = self.service.search_available_appointments(
            clinic_type="medical"
        )
        self.assertEqual(len(results), 2)

    def test_combined_filters(self):
        results = self.service.search_available_appointments(
            appointment_date=date(2026, 11, 5),
            clinic_type="dental"
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, 102)

    def test_booked_appointments_excluded(self):
        results = self.service.search_available_appointments()

        ids = [slot.id for slot in results]
        self.assertNotIn(104, ids)

    def test_no_matching_appointments(self):
        results = self.service.search_available_appointments(
            appointment_date=date(2026, 11, 10)
        )
        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
