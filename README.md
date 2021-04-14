## Vence Garage

This is a simple implementation of a garage, a tool that helps tracking the veicles that goes in and out a garage.

This project is made of 4 separate Docker containers that holds:

- PostgreSQL database
- Flask backend (SQLAlchemy ORM)
- Vue.js frontend
- Nginx

---

### Prerequisites

In order to run this application you need to install two tools: **Docker** & **Docker Compose**.

Instructions how to install **Docker** on [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/), [Windows](https://docs.docker.com/docker-for-windows/install/), [Mac](https://docs.docker.com/docker-for-mac/install/).

**Docker Compose** is already included in installation packs for *Windows* and *Mac*, so only Ubuntu users needs to follow [this instructions](https://docs.docker.com/compose/install/).

### How to run it?
Run the following commands
```
$ docker-compose up --build -d
$ docker-compose run backend /usr/local/bin/python create_db.py
```

To run the tests
```
$ docker-compose run backend /usr/local/bin/pytest tests.py
```
If you want to stop it, use the following command:

```
$ docker-compose down
```

---

### database (Database)

PostgreSQL database contains only single schema with four tables - Level, VehicleType, ParkingSpot and Reservation.

Like other parts of application Postgres database is containerized and
the definition of its Docker container can be found in
*docker-compose.yml* file.

```yml
postgres:
    restart: always
    image: postgres:13-alpine
    volumes:
      - db-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    environment:
      POSTGRES_HOST_AUTH_METHOD: trust
```

### backend (REST API)

This is a Flask application that connects with a
database and expose the REST endpoints that can be consumed by
frontend.
The backend will be running on http://localhost:8000/

The admin dashboard can be accessed on http://localhost:8000/admin/
Open endpoints

* [ReserveSpot](.apidoc/reserve.md) : `POST /reserve/`
* [CheckoutVehicle](.apidoc/checkout.md) : `POST /checkout/`
* [StatusReport](.apidoc/status.md) : `GET /status/`
* [CurrentVehicles](.apidoc/current.md) : `GET /current/`
* [GetVehicleTypes](.apidoc/vtypes.md) : `GET /vtypes/`

FOR TESTING ONLY
* [InitDB](md/.apidoc/init.md) : `POST /init/`

This app is also put in Docker container and its definition can be found
in a file *backend/Dockerfile*. 



### frontend

It's the UI that consumes the REST API endpoints provided by
*backend*.

It can be entered using link: **http://localhost/**

#### nginx

The entry point, allows access to the frontend and the backend.

its Docker container can be found in
*docker-compose.yml* file.

```yml
nginx:
    restart: always
    build: ./nginx
    ports:
      - "80:80"
      - "8000:8000"
    links:
      - backend:backend
```