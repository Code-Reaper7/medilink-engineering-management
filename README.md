# medilink-engineering-management

Software Engineering Management assignment simulating the development workflow, coordination, incident management, and continuous improvement of the MediLink Appointment Platform.

## **Work in Progress (WIP) Limit**

The MediLink team has established a **WIP limit of 3 tasks** in the In Progress column.

This limit was selected because the team consists of four members, including one Engineering Manager. Limiting active development to three tasks helps prevent excessive multitasking, reduces context switching, and encourages developers to complete existing work before starting new tasks.

When the WIP limit is reached, team members should prioritize completing current tasks, resolving blockers, or assisting with code reviews instead of starting additional work.

The Engineering Manager will monitor WIP during the development cycle and help maintain a balanced workflow.

## Team workflow and responsibilities

The project follows the workflow **Backlog → Ready → In Progress → Code Review → Verification → Done**.

The current team is structured as follows:

- Farhan: Engineering Manager and technical contributor for the rescheduling work
- Hamido: defect fix for double-booking of appointment slots
- Omar: booking validation and testing work
- Alex: API and developer documentation updates

## Booking safeguards

Each appointment slot accepts only one confirmed booking. A booking attempt for an
already-booked slot is rejected, and cancelling an appointment more than once is
ignored so it cannot release a slot that another patient has booked.

Simultaneous booking attempts are out of scope for this in-memory implementation;
handling them safely would require concurrency control or a transactional
persistent data store.
