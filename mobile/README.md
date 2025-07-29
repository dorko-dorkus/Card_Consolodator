# Consolidator Mobile

This directory contains the Expo-based mobile client. The project is a simple starting point that can be expanded as features are implemented.

## Getting Started

1. Install dependencies
   ```bash
   npm install
   ```
2. Start the development server
   ```bash
   npx expo start
   ```

Use the on-screen options to run the app on a simulator, physical device or in the browser.

## Login feature

The app now starts on a **Login** screen. Provide your registered email and
password and press **Login**. On success you will be taken to the home screen
which fetches session information from the backend.

From the home screen you can navigate to additional flows:

- **Gift Cards** – lists the user's gift cards and offers a button to consolidate them.
- **Link Bank Account** – allows submitting a bank token to link via the backend.
- **Make Purchase** – submit an amount and payment token to create a purchase.

Ensure the backend server is running and accessible before attempting to log in.

### Configuring the backend URL

API requests default to `http://localhost:5000`. To point the mobile client at a
different backend, set the `BACKEND_URL` environment variable when starting the
development server:

```bash
BACKEND_URL="http://192.168.1.42:8000" npx expo start
```

This value is read in `api.js` and used as the base URL for all network calls.

### Running tests

Run the Jest test suite with:

```bash
npm test
```

### Building a release

Install the EAS CLI and build for Android or iOS:

```bash
npm install -g eas-cli
eas login
eas build --platform android  # or ios
```

Provide environment variables such as `BACKEND_URL` or `STRIPE_PUBLISHABLE_KEY`
via an `eas.json` profile or `--env` flags when building.
