import React from "react";
import { View, Button, Text } from "react-native";
import { useStripe } from "@stripe/stripe-react-native";
import { saveItem, getItem } from "./SecureStore";

const PaymentScreen = () => {
  const { presentGooglePay } = useStripe();

  React.useEffect(() => {
    (async () => {
      const method = await getItem("last_payment_method");
      if (method) {
        console.log("Last payment method:", method);
      }
    })();
  }, []);

  const handleGooglePay = async () => {
    const { error, paymentMethod } = await presentGooglePay({
      currencyCode: "USD",
      amount: 1000, // $10.00
    });
    if (error) {
      console.log("Payment failed:", error);
    } else {
      console.log("Payment successful!");
      if (paymentMethod?.id) {
        await saveItem("last_payment_method", paymentMethod.id);
      }
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
