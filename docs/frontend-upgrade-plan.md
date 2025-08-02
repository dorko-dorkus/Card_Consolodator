# Frontend Package Upgrade Plan

This document lists outdated dependencies for the React Native apps and proposes steps to upgrade.

## Current versions

### Frontend (Expo Router app)

- **Expo**: 52.x (latest 53.x)
- **React Native**: 0.76.7 (latest 0.80.2)
- **React**: 18.2.0 (latest 19.1.1)

Other libraries with updates include:

- @stripe/stripe-react-native (latest 0.50.1)
- expo-router (latest 5.1.4)
- expo-secure-store (latest 14.2.3)
- expo-splash-screen (latest 0.30.10)
- react-native-safe-area-context (latest 5.5.2)
- react-native-webview (latest 13.15.0)

### Mobile directory

- **Expo**: 52.x (latest 53.x)
- **React Native**: 0.76.7 (latest 0.80.2)
- **React**: 18.2.0 (latest 19.1.1)
- @react-navigation libraries and others also have newer versions available.

## Recommended upgrade steps

1. **Prepare for Expo 53**
   - Review the [Expo SDK 53 release notes](https://blog.expo.dev/expo-sdk-53-is-now-available-d176053dc842) for breaking changes.
   - Update `expo` and related packages by editing `package.json` and running `npm install` as the `expo upgrade` command has been deprecated.
   - Ensure the `eas-cli` version is up to date if you use EAS build.

2. **Upgrade React Native**
   - After upgrading Expo, React Native will move to the version bundled with Expo 53 (currently 0.73). The repo currently uses bare React Native 0.76 in `package.json`, so align the version with Expo or move to an Expo prebuild workflow.
   - For the bare `mobile` app, follow the [React Native upgrade helper](https://react-native-community.github.io/upgrade-helper/) to jump from 0.76 to 0.80, resolving any breaking changes in native code.

3. **Update navigation and other libraries**
   - Upgrade `@react-navigation` packages to the latest major release and run tests to catch any API changes.
   - Update the Stripe SDK and other Expo modules (`expo-secure-store`, `expo-splash-screen`, etc.) after confirming compatibility with the new Expo/React Native versions.

4. **Run automated tests**
   - Execute `npm test` in both `frontend` and `mobile` directories to verify functionality after each upgrade step.
   - Fix any failing tests and address deprecation warnings.

5. **Update documentation**
   - Document the new versions and any required configuration changes in `README.md`.
   - A convenience `upgrade` script has been added to each React Native project's `package.json`.
     Run `npm run upgrade` in the `frontend` or `mobile` directories to refresh dependencies with `npm update` for future updates.

These upgrades will keep the app on supported versions and ensure access to the latest features and security fixes.
