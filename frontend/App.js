
import React, { useEffect, useState, useContext } from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import HomeScreen from "./HomeScreen";
import ConsolidationScreen from "./ConsolidationScreen";
import PaymentScreen from "./PaymentScreen";
import BankAccountScreen from "./BankAccountScreen";
import TopUpScreen from "./TopUpScreen";
import PurchaseScreen from "./PurchaseScreen";
import LoginScreen from "./LoginScreen";
import RegisterScreen from "./RegisterScreen";
import { StripeProvider } from "@stripe/stripe-react-native";
import { getItem, saveItem } from "./SecureStore";
import { AuthProvider, AuthContext } from "./AuthContext";

const STRIPE_KEY_STORAGE = "stripe_publishable_key";

const AppNavigator = () => {
  const { user, loading } = useContext(AuthContext);
  const Stack = createStackNavigator();

  if (loading) return null;

  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName={user ? 'Home' : 'Login'}>
        {user ? (
          <>
            <Stack.Screen name="Home" component={HomeScreen} />
            <Stack.Screen name="Consolidate" component={ConsolidationScreen} />
            <Stack.Screen name="Checkout" component={PaymentScreen} />
            <Stack.Screen name="BankAccounts" component={BankAccountScreen} />
            <Stack.Screen name="TopUp" component={TopUpScreen} />
            <Stack.Screen name="Purchase" component={PurchaseScreen} />
          </>
        ) : (
          <>
            <Stack.Screen name="Login" component={LoginScreen} />
            <Stack.Screen name="Register" component={RegisterScreen} />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
};

const App = () => {
  const [publishableKey, setPublishableKey] = useState(null);

  useEffect(() => {
    (async () => {
      let key = process.env.STRIPE_PUBLISHABLE_KEY;
      if (!key) {
        key = await getItem(STRIPE_KEY_STORAGE);
      }
      if (!key) {
        // Default publishable key used for development/testing
        key = "your-publishable-key";
        await saveItem(STRIPE_KEY_STORAGE, key);
      }
      setPublishableKey(key);
    })();
  }, []);

  if (!publishableKey) {
    return null; // or a splash screen
  }

  return (
    <StripeProvider publishableKey={publishableKey}>
      <AuthProvider>
        <AppNavigator />
      </AuthProvider>
    </StripeProvider>
  );
};

export default App;
