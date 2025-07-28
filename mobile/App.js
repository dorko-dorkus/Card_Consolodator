import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import LoginScreen from './LoginScreen';
import HomeScreen from './HomeScreen';
import GiftCardListScreen from './GiftCardListScreen';
import BankLinkScreen from './BankLinkScreen';
import PurchaseScreen from './PurchaseScreen';

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Login">
        <Stack.Screen name="Login" component={LoginScreen} options={{ headerShown: false }} />
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="GiftCards" component={GiftCardListScreen} />
        <Stack.Screen name="BankLink" component={BankLinkScreen} />
        <Stack.Screen name="Purchase" component={PurchaseScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

