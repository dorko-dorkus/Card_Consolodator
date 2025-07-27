
import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import HomeScreen from "../screens/HomeScreen";
import ConsolidationScreen from "../screens/ConsolidationScreen";
import PaymentScreen from "../screens/PaymentScreen";
import { StripeProvider } from "@stripe/stripe-react-native";

const Stack = createStackNavigator();

const App = () => {
  return (
    <StripeProvider publishableKey="your-publishable-key">
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
