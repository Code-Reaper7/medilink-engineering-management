# MediLink API / Developer Docs

Docs for issue #8. Everything here is about `MediLinkService` in `medilink.py`. There's no real server or database, it's all in memory, so the "API" is just the methods on that class.

## Setup

You only need Python 3, nothing to install.

```bash
git clone https://github.com/Code-Reaper7/medilink-engineering-management.git
cd medilink-engineering-management
python -m unittest discover -s tests -v
```

(`python -m pytest` works too if you have pytest.)

## How the data is stored

- `slots`: dict of slot id -> `AppointmentSlot` (id, clinic_type, starts_at, booked)
- `appointments`: dict of appointment id -> `Appointment` (id, slot_id, status). status is either `"booked"` or `"cancelled"`
- `reminder_queue`: set of appointment ids that still need a reminder

## Methods

All the examples use this setup:

```python
from datetime import datetime, date
from medilink import MediLinkService

service = MediLinkService()
service.add_slot(101, "medical", datetime(2026, 11, 5, 10, 0))
service.add_slot(102, "medical", datetime(2026, 11, 6, 14, 0))
service.add_slot(103, "dental", datetime(2026, 11, 6, 11, 0))
```

### add_slot(slot_id, clinic_type, starts_at)

Adds a free slot. Doesn't return anything. Careful: using an id that already exists overwrites the old slot (see known issues at the bottom).

### book_appointment(appointment_id, slot_id)

Books the slot, marks it as booked and puts the appointment in the reminder queue.

Raises `ValueError` if:
- the appointment id is already used -> "Appointment already exists"
- the slot doesn't exist -> "Appointment slot not found"
- the slot is already taken -> "Appointment slot unavailable"

```python
service.book_appointment(1, 101)
service.book_appointment(2, 101)  # ValueError: Appointment slot unavailable
```

### cancel_appointment(appointment_id)

Sets the status to cancelled, frees the slot and removes the reminder from the queue. If it's already cancelled nothing happens, so cancelling twice can't free a slot someone else booked after (that was the #4 bug).

An id that doesn't exist gives a `KeyError`.

```python
service.book_appointment(1, 101)
service.cancel_appointment(1)
service.slots[101].booked      # False
service.cancel_appointment(1)  # does nothing
```

### send_reminders()

Returns the ids in the queue that are still booked (sorted), then empties the queue. It checks the status right before "sending", so a cancelled appointment that's somehow still in the queue gets skipped (#1). Nothing actually gets sent, it just returns the ids.

```python
service.book_appointment(1, 101)
service.book_appointment(2, 102)
service.cancel_appointment(2)
service.send_reminders()  # [1]
service.send_reminders()  # [] because the queue got cleared
```

### search_available_appointments(appointment_date=None, clinic_type=None)

Returns free slots sorted by time. You can filter by date (a `date` object), clinic type (not case sensitive), both, or neither.

```python
[s.id for s in service.search_available_appointments()]  # [101, 103, 102]
[s.id for s in service.search_available_appointments(date(2026, 11, 6), "Medical")]  # [102]
```

### reschedule_appointment(appointment_id, new_slot_id)

Moves a booked appointment to a different free slot. The old slot becomes free again and the reminder stays queued. Returns a dict:

```python
service.book_appointment(1, 101)
service.reschedule_appointment(1, 102)
# {'appointment_id': 1, 'old_slot_id': 101, 'new_slot_id': 102,
#  'message': 'Appointment rescheduled successfully'}
```

Raises `ValueError` with one of these:
- "Appointment not found"
- "Cannot reschedule a cancelled appointment"
- "Appointment slot not found"
- "Please select a different time slot" (same slot as before)
- "Appointment slot unavailable"

## Tests

| file | what it tests | issue |
|---|---|---|
| test_medilink.py | reminders + cancelling | #1 |
| test_appointment_search.py | search filters | #2 |
| test_appointment_rescheduling.py | rescheduling | #3 |
| test_double_booking.py | double booking | #4 |
| test_booking_validation.py | booking validation | #5 |

## Logging and incident monitoring

Configure logging at the application entry point:

```python
from medilink import configure_logging

configure_logging()
```

Appointment booking, cancellation, and reminder processing emit JSON log entries
with timestamps, operation names, identifiers, and failures. Error entries use
`ERROR` level and include the exception type and message. Logs contain no patient
names, contact details, clinical details, or other patient information.

For a lightweight production check, send application logs to the service's
central log destination and alert on `level=ERROR` with events ending in
`_failed`. During an incident, filter by the event and appointment/slot
identifier, record the timestamp and error message, then reproduce the failure
with the relevant appointment test before closing the incident. Never copy
patient information into log messages or incident tickets.

Before something goes to Done:
1. run all the tests locally before opening the PR
2. put "Closes #N" in the PR and say what you tested
3. request a reviewer when you open it, don't merge without an approve
4. after it's merged, someone runs the tests on main again and comments on the issue with what they checked
5. then move it to Done (see [Definition_of_Done.md](Definition_of_Done.md))

## Known issues

- everything is in memory, it's gone when the program stops
- no real notifications, send_reminders just returns ids
- two people booking at the exact same time isn't handled (would need locking or a real db)
- cancelling an id that doesn't exist throws KeyError instead of a ValueError like everything else
- add_slot with an id that already exists resets it to free even if someone booked it, so it could get double booked
