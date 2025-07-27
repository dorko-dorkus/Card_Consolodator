# Consolidator Project

This repository contains both the front-end and back-end code for the Consolidator application.

* `frontend/` – an [Expo](https://expo.dev) React Native app.
* `backend/` – a Flask API server.

Each part can be run and developed independently.

## Get started (frontend)

1. Install dependencies

   ```bash
   npm install
   ```

2. Set your Stripe publishable key (required)

   ```bash
   export STRIPE_PUBLISHABLE_KEY=your-publishable-key
   ```

3. Start the app

   ```bash
    npx expo start
   ```

In the output, you'll find options to open the app in a

- [development build](https://docs.expo.dev/develop/development-builds/introduction/)
- [Android emulator](https://docs.expo.dev/workflow/android-studio-emulator/)
- [iOS simulator](https://docs.expo.dev/workflow/ios-simulator/)
- [Expo Go](https://expo.dev/go), a limited sandbox for trying out app development with Expo

You can start developing by editing the files inside the **app** directory. This project uses [file-based routing](https://docs.expo.dev/router/introduction).

## Get a fresh project

When you're ready, run:

```bash
npm run reset-project
```

This command will move the starter code to the **app-example** directory and create a blank **app** directory where you can start developing.

### Secure credentials

The Expo application stores the Stripe publishable key and recent payment tokens
using `expo-secure-store`. Storing these values in the device keychain keeps
credentials out of the codebase and adds a layer of security. You can also
provide a `STRIPE_PUBLISHABLE_KEY` environment variable when starting the app;
the value will be used before falling back to the stored credentials.

### Building Android and iOS releases

1. Install the EAS CLI and log in:

   ```bash
   npm install -g eas-cli
   eas login
   ```

2. Configure your signing credentials. Expo can manage them for you:

   ```bash
   eas build:configure --platform android
   eas build:configure --platform ios
   ```

   Follow the prompts to generate or provide keystores, certificates and provisioning profiles.

3. Run a production build:

   ```bash
   # Android
   eas build --platform android

   # iOS
   eas build --platform ios
   ```

   The legacy `expo build:android` and `expo build:ios` commands also work if you prefer.

4. Provide environment variables such as `STRIPE_PUBLISHABLE_KEY` and `BACKEND_URL` when
   building. You can define them in an `eas.json` profile or pass them on the command line:

   ```json
   {
     "build": {
       "production": {
         "env": {
           "STRIPE_PUBLISHABLE_KEY": "pk_live_your_key",
           "BACKEND_URL": "https://api.example.com"
         }
       }
     }
   }
   ```

   Running `eas build --profile production` will then inject these values at build time.

## Get started (backend)

```bash
cd backend
pip install -r requirements.txt
# For development
python run.py
# For production
gunicorn wsgi:app
```

### Docker

You can build the API server into a container using the provided Dockerfile:

```bash
docker build -t consolidator-backend ./backend
docker run --env-file backend/.env -p 8000:8000 consolidator-backend
```

A `docker-compose.yml` file is included to run the backend together with a
persistent Redis instance used by Flask-Limiter:

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000` and Redis data will be
stored in the `redis-data` volume. When the services are running you can
verify that `RATELIMIT_STORAGE_URL` and the variables from `.env` were passed
to the container:

```bash
docker compose exec backend env | grep RATELIMIT_STORAGE_URL
```

Before starting the server, create a `.env` file for your local secrets:

```bash
cp backend/.env.example backend/.env
# then edit backend/.env and add your real credentials
```

Make sure to define an `ENCRYPTION_KEY` in this file or in your environment. The
example file `backend/.env.example` shows the variable name. This key is used to
encrypt sensitive data stored by the API.

The server uses [Flask-CORS](https://flask-cors.readthedocs.io/) to allow
cross-origin requests. Set the `CORS_ORIGINS` environment variable to a
comma-separated list of allowed origins (defaults to `*`).

### Logging and rate limiting

The API configures Python logging to write to STDOUT by default. Set a `LOG_FILE`
environment variable if you prefer writing logs to a file. Unexpected errors are
logged with full stack traces.

All routes are protected by [Flask-Limiter](https://flask-limiter.readthedocs.io/)
with a default limit of `100/hour` per IP. Adjust this by setting the
`RATE_LIMIT` environment variable, e.g. `RATE_LIMIT=10/minute`.

Your `DATABASE_URL` should use a standard SQLAlchemy connection string. For example:

* **Postgres**: `postgresql://user:password@hostname:5432/dbname`
* **MySQL**: `mysql+pymysql://user:password@hostname:3306/dbname`

## Database migrations

Flask-Migrate commands are available through `manage.py`. To create or apply
migrations run:

```bash
cd backend
export FLASK_APP=manage.py
flask db upgrade  # apply existing migrations
```

Use `flask db migrate -m "Message"` to generate new migration scripts when your
models change.

### Gift card management endpoints

You can add physical or imported gift cards to a user's account using the
`/api/gift-cards` endpoint.

```
POST /api/gift-cards
{
  "user_id": 1,
  "card_number": "123456789012",
  "balance": 50,
  "expiry_date": "2099-12-31",
  "source": "physical_card"  # or "imported_card"
}
```

The API validates the card number format and ensures the expiry date is in the
future before storing the card.

## Learn more

To learn more about developing your project with Expo, look at the following resources:

- [Expo documentation](https://docs.expo.dev/): Learn fundamentals, or go into advanced topics with our [guides](https://docs.expo.dev/guides).
- [Learn Expo tutorial](https://docs.expo.dev/tutorial/introduction/): Follow a step-by-step tutorial where you'll create a project that runs on Android, iOS, and the web.

## Join the community

Join our community of developers creating universal apps.

- [Expo on GitHub](https://github.com/expo/expo): View our open source platform and contribute.
- [Discord community](https://chat.expo.dev): Chat with Expo users and ask questions.

## Deployment

Create a `backend/.env` file before running the API in production. Copy the
example file and replace each placeholder with your real credentials.  The
application uses PostgreSQL in production, so set `DATABASE_URL` to the
connection string for your Postgres instance (for example
`postgresql://user:password@localhost:5432/consolidator`):

```bash
cp backend/.env.example backend/.env
# edit backend/.env and set values for:
#   SECRET_KEY
#   DATABASE_URL
#   STRIPE_SECRET_KEY
#   STRIPE_PUBLISHABLE_KEY
#   STRIPE_WEBHOOK_SECRET
#   JWT_SECRET_KEY
#   ENCRYPTION_KEY
#   CORS_ORIGINS
```

After creating the environment file, apply the migrations to set up the
database schema:

```bash
cd backend
export FLASK_APP=manage.py
flask db upgrade
```

When deploying with Docker Compose or `docker run`, pass this file using the
`--env-file` option:

```bash
docker compose up      # uses env_file in docker-compose.yml
docker run --env-file backend/.env -p 8000:8000 consolidator-backend
```

### Running behind a production web server

For production deployments run the API with Gunicorn and place a reverse proxy
like Nginx in front of it. Gunicorn should bind to a local interface so the
proxy can forward requests:

```bash
gunicorn wsgi:app --workers 4 --bind 127.0.0.1:8000
```

A minimal Nginx configuration might look like this:

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

This keeps Gunicorn behind the reverse proxy while still serving the API on
port 80.

