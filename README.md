## Backend

To run the backend, first set up the `.env` file with your own data:

1. `cp backend/.env.example backend/.env`
2. Update the `backend/.env` data

Build and run the app containers:

1. `make build`
2. `make run`

Or alternatively: `make reset` (re-builds and brings up the containers)

To stop the containers: `make stop`

### App commands

Django related commands:

- `make test`: runs all the backend tests
- `make test <path>`: runs the specified `<path>` tests (e.g. `make test reviews.tests`)
- `make migrations`: creates the Django migrations
- `make migrate`: migrates the backend database
- `make createsuperuser`: adds a new super user to the DB

Other commands:

- `make format`: formats the backend code (using `black`)
- `make requirements`: updates the `requirements.tsx`file
