import React, { useState } from "react";
import { View, Text, TextInput, Button } from "react-native";
import { makePurchase } from "./api";

const PurchaseScreen = () => {
  const [amount, setAmount] = useState("");
  const [message, setMessage] = useState("");

  const handlePurchase = async () => {
    const result = await makePurchase(1, parseFloat(amount));
    if (result?.remaining_balance !== undefined) {
      setMessage(`Remaining balance: $${result.remaining_balance}`);
    } else if (result?.error) {
      setMessage(result.error);
    }
  };

  return (
    <View style={{ flex: 1, padding: 20 }}>
      <Text style={{ fontSize: 24, fontWeight: "bold" }}>Purchase</Text>
      <TextInput
        placeholder="Amount"
        value={amount}
        onChangeText={setAmount}
        keyboardType="numeric"
        style={{ borderWidth: 1, padding: 8, marginVertical: 10 }}
      />
      <Button title="Make Purchase" onPress={handlePurchase} />
      {message ? <Text style={{ marginTop: 20 }}>{message}</Text> : null}
    </View>
  );
};

export default PurchaseScreen;
