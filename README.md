# num_service

## Overview

The **Num Service** is a Django-based API that provides numeric-based computations, including:

- `/difference?number=<int>`

  To calculate the difference between the sum of squares and the square of sums for a given `number`.

- `/pythagorean?number=<int>`

  To calculate Pythagorean triplets where the product of `(a, b, c)` matches a given `number`.

## Installation & Setup

Let's start with a method to run the Django server locally (directly on your laptop and not in a container).
There is another alternative below to run everything in a dockerized environment (including the Django server)

As you've probably noticed, you'll need Docker installed in your computer to run this command.
You should be able to find instructions on how to install it in [this link](https://docs.docker.com/desktop/).

1. Clone the Repository

    ```shell
    git clone git@github.com:Savir/num_service.git
    cd num_service/num_service/
    ```

2. Start the Postgres database (and the migrator)

   Assuming you are located in the (second) `num_service/` directory, do:
    ```shell
    docker compose --file ./docker-compose.db.yaml up --build
    ```
   This will start a Postgres database and apply the most up to date migrations. All via docker containers.

   Once the migrator "job" (container, really) has finished running, you should be safe to continue. You should see
    ```shell
   migrator-1    | Running migrations:
   migrator-1    |   Applying pythagorean_triplet.0001_initial... OK
   migrator-1    |   Applying squares_diff.0001_initial... OK
   migrator-1 exited with code 0
    ```
   The important part is that the migrator ran successfully (that's what _"exited with code 0"_ mean)

   The only thing the migrator really does is generating the pending migrations (which should be none, because all of
   them should've been commited by the developers working on this) and apply them. Meaning:
   ```shell
   python manage.py makemigrations \
   && python manage.py migrate
   ```
   Nothing you can't do manually once Django is installed... but this way should be more convenient, right?

   ⚠️ This method will leave docker running in the foreground, so you will need to open another terminal
   in the same `num_service/num_service/` directory for the next steps.

3. Install required packages
   Run pip to install the backend's requirements:
   ```shell
   pip3 install --requirement=backend/requirements.txt
   ```
   Running the command above will install the project's requirements globally, but it's highly recommended using
   Virtual Environments. Virtual Environments help isolate dependencies, ensuring the installed packages are only for
   this project. This prevents conflicts with system-wide packages. You can refer to
   [this page](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) for
   more details, but here's a quick reference:
   ```shell
   python3 -m venv .num_service_venv \
   && source .num_service_venv/bin/activate \
   && .num_service_venv/bin/pip3 install --requirement=backend/requirements.txt
   ```

4. Launch the Django test server
   ```shell
   python ./backend/manage.py runserver 127.0.0.1:8000
   ```
   This will launch a server accepting incoming requests from your local computer (`127.0.0.1` a.k.a. `localhost`)
   on port `8000`. Otherwise said, you should be able to open your favorite browser type `http://127.0.0.1:8000/`
   or `http://localhost:8000/` in the address bar and reach the Django server. You should probably see a (fairly
   pretty) _"Page not found"_ error page but that's actually a good sign! It means there's a Django server listening on
   the other end.

   You could also use `curl` in a terminal, if you have it installed:
   ```shell
   curl --request GET "http://localhost:8000" 
   ```
   You should see some HTML code printed on the terminal. That's the _"Page not found"_ error
   page. Not as pretty this way, right?

   Note that the database connection data defaults to the database exposed by Docker.
   See the [`DATABASES` section in ./num_service/backend/core/settings.py](./num_service/backend/core/settings.py).
   You can change that by providing a different connection URL via the `DATABASE_URL` environment variable.
   For instance, let's say your username is... `pguser`, the database password is `foo` (safety over all!)
   the database to use for this project (which, by the way: should be created in the PostgreSQL server) is
   called `mydb` and the DB server is listening for connections on port `54320`, instead of to the
   default `5432` for PostgreSQL.
   You could launch Django to use that connection configuration by doing:
   ```shell
   DATABASE_URL="postgres://pguser:foo@postgres:54320/mydb" python ./backend/manage.py runserver 127.0.0.1:8000
   ```


5. Test an endpoint.

   Send a request to, for instance, the `/difference` service:
   ```shell
   curl --request GET "http://localhost:8000/difference?number=10"
   ```
   will print the Json response:
   ```json
   {"datetime":"2025-02-14T03:52:01.368049Z","value":2640,"number":10,"occurrences":2,"last_datetime":"2025-02-14T03:42:36.719290Z"}
   ```

Now, there's a second method that will not require you to install packages locally
and that is running everything in Docker.

Should be as easy as:

```shell
git clone git@github.com:Savir/num_service.git \
&& cd num_service/num_service/ \
&& docker compose up --build
```

Once you see the line...

```shell
backstage_backend  | Watching for file changes with StatReloader
```

... the server should be ready to accept connections.

Since docker compose exposes port `8000` from the container into the host, you
should be able to reach the Django server, running in the `backend` container
the same as with the method above:

```shell
   curl --request GET "http://localhost:8000/pythagorean?number=60"
```

## Running tests

If your Django server is running locally (not in docker) you can run

```shell
cd ./backend/ \
&& python manage.py test
```

If the Django server is running in a Docker container (which should be named `backstage_backend`), you can do:

```shell
docker exec backstage_backend python /backend/manage.py test
```

## API Responses:

The API responses contain the following common fields:

- **`datetime`**: The timestamp indicating when the current request was processed.
- **`number`**: The number the calculations were performed for (the query parameter provided in the URL by
  the user utilizing the API).
- **`occurrences`**: The number of times this specific number has been requested in this service.
  Each service (Pythagorean and Square Difference) tracks occurrences separately.
- **`last_datetime`**: The timestamp of the previous request for this `number` in the same
  service (tracked independently per service).

#### Samples:

##### 1. Difference of Squares API

```sh
curl -X GET "http://localhost:8000/difference?number=10"
```

**Response:**

```json
{
  "datetime": "2025-02-14T15:05:03.949166Z",
  "value": 2640,
  "number": 10,
  "occurrences": 1,
  "last_datetime": "2025-02-14T15:05:03.946383Z"
}
```

##### 2. Pythagorean Triplet API

```sh
curl -X GET "http://localhost:8000/pythagorean?number=20580"
```

**Response:**

```json
{
  "datetime": "2025-02-14T15:05:34.562492Z",
  "triplet": {
    "a": 21,
    "b": 28,
    "c": 35
  },
  "number": 20580,
  "occurrences": 1,
  "last_datetime": "2025-02-14T15:05:34.558862Z"
}
```

If a triplet could not be found, it's value will still exist, but will be `null`:

```sh
curl -X GET "http://localhost:8000/pythagorean?number=10"
```

```json
{
  "datetime": "2025-02-14T15:06:35.832997Z",
  "triplet": null,
  "number": 10,
  "occurrences": 1,
  "last_datetime": "2025-02-14T15:06:35.830311Z"
}
```

## Design Considerations

This project was designed with future extensibility in mind. While the current functionality could be
implemented with a couple of simple views, we structured it with scalability in mind.

To accommodate potential growth and multiple feature additions, we made the following choices:

- **Modular Architecture**: Created two separate Django apps (one per endpoint) to allow independent development.
  This structure enables multiple teams to work on different services with minimal conflicts.
- **Django REST Framework (DRF)**: Chosen to provide a robust API foundation. As additional functionalities and
  methods are introduced, DRF will help streamline development and maintain consistency.

This design ensures the system can easily integrate more numeric queries beyond the ones currently implemented.
