import React, { useState, useContext } from "react";
import { View, TextInput, Button, StyleSheet } from "react-native";
import { makePurchase } from "./api";
import { ThemedText } from "./ThemedText";
import { useColorScheme } from "./hooks/useColorScheme";
import { Colors } from "./constants/Colors";
import { AuthContext } from "./AuthContext";

const PurchaseScreen = () => {
  const { user } = useContext(AuthContext);
  const [amount, setAmount] = useState("");
  const [message, setMessage] = useState("");
  const theme = useColorScheme() ?? "light";
  const tint = Colors[theme].tint;

  const handlePurchase = async () => {
    if (!user) return;
    const result = await makePurchase(user.user_id, parseFloat(amount));
    if (result?.remaining_balance !== undefined) {
      setMessage(`Remaining balance: $${result.remaining_balance}`);
    } else if (result?.error) {
      setMessage(result.error);
    }
  };

  return (
    <View style={[styles.container, { backgroundColor: Colors[theme].background }] }>
      <ThemedText style={styles.title}>Purchase</ThemedText>
      <TextInput
        placeholder="Amount"
        value={amount}
        onChangeText={setAmount}
        keyboardType="numeric"
        style={styles.input}
      />
      <Button color={tint} title="Make Purchase" onPress={handlePurchase} />
      {message ? <ThemedText style={styles.message}>{message}</ThemedText> : null}
    </View>
  );
};

export default PurchaseScreen;

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
  input: {
    borderWidth: 1,
    padding: 8,
    marginVertical: 10,
    borderRadius: 6,
  },
  message: {
    marginTop: 20,
  },
});
