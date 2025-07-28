import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { COLORS } from './theme';
import LoginScreen from './LoginScreen';
import HomeScreen from './HomeScreen';
import GiftCardListScreen from './GiftCardListScreen';
import BankLinkScreen from './BankLinkScreen';
import PurchaseScreen from './PurchaseScreen';

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Login"
        screenOptions={{
          headerStyle: { backgroundColor: COLORS.primary },
          headerTintColor: '#fff',
          headerTitleAlign: 'center',
        }}
      >
        <Stack.Screen
          name="Login"
          component={LoginScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen name="Home" component={HomeScreen} options={{ title: 'Home' }} />
        <Stack.Screen name="GiftCards" component={GiftCardListScreen} options={{ title: 'Gift Cards' }} />
        <Stack.Screen name="BankLink" component={BankLinkScreen} options={{ title: 'Link Bank Account' }} />
        <Stack.Screen name="Purchase" component={PurchaseScreen} options={{ title: 'Purchase' }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

