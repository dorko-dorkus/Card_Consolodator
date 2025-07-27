import React from "react";
import { View, Button, StyleSheet } from "react-native";
import { useStripe } from "@stripe/stripe-react-native";
import { saveItem, getItem } from "./SecureStore";
import { ThemedText } from "./ThemedText";
import { useColorScheme } from "./hooks/useColorScheme";
import { Colors } from "./constants/Colors";

const PaymentScreen = () => {
  const { presentGooglePay } = useStripe();
  const theme = useColorScheme() ?? "light";
  const tint = Colors[theme].tint;

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
    <View style={[styles.container, { backgroundColor: Colors[theme].background }] }>
      <ThemedText style={styles.title}>Tap to Pay</ThemedText>
      <Button color={tint} title="Pay with Google Pay" onPress={handleGooglePay} />
    </View>
  );
};

export default PaymentScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    justifyContent: "center",
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 20,
  },
});
