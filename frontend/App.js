
import React, { useEffect, useState } from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import HomeScreen from "../screens/HomeScreen";
import ConsolidationScreen from "../screens/ConsolidationScreen";
import PaymentScreen from "../screens/PaymentScreen";
import { StripeProvider } from "@stripe/stripe-react-native";
import { getItem, saveItem } from "./SecureStore";

const Stack = createStackNavigator();

const STRIPE_KEY_STORAGE = "stripe_publishable_key";

const App = () => {
  const [publishableKey, setPublishableKey] = useState(null);

  useEffect(() => {
    (async () => {
      let key = await getItem(STRIPE_KEY_STORAGE);
      if (!key) {
        key = "your-publishable-key"; // fallback for development
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
      <NavigationContainer>
        <Stack.Navigator initialRouteName="Home">
          <Stack.Screen name="Home" component={HomeScreen} />
          <Stack.Screen name="Consolidate" component={ConsolidationScreen} />
          <Stack.Screen name="Checkout" component={PaymentScreen} />
        </Stack.Navigator>
      </NavigationContainer>
    </StripeProvider>
  );
};

export default App;
