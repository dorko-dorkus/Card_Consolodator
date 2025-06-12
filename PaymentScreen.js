import React from "react";
import { View, Button, Text } from "react-native";
import { useStripe } from "@stripe/stripe-react-native";

const PaymentScreen = () => {
  const { presentGooglePay } = useStripe();

  const handleGooglePay = async () => {
    const { error } = await presentGooglePay({
      currencyCode: "USD",
      amount: 1000, // $10.00
    });
    if (error) {
      console.log("Payment failed:", error);
    } else {
      console.log("Payment successful!");
    }
  };

  return (
    <View style={{ flex: 1, padding: 20 }}>
      <Text style={{ fontSize: 24, fontWeight: "bold" }}>Tap to Pay</Text>
      <Button title="Pay with Google Pay" onPress={handleGooglePay} />
    </View>
  );
};

export default PaymentScreen;
