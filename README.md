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

2. Start the app

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
credentials out of the codebase and adds a layer of security.

## Get started (backend)

```bash
cd backend
pip install -r requirements.txt
python run.py
```

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
