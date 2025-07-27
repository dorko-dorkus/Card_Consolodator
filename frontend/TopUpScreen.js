import React, { useState } from "react";
import { View, Text, TextInput, Button } from "react-native";
import { transferFromBank } from "./api";

const TopUpScreen = () => {
  const [accountId, setAccountId] = useState("");
  const [amount, setAmount] = useState("");
  const [message, setMessage] = useState("");

  const handleTransfer = async () => {
    const result = await transferFromBank(1, accountId, parseFloat(amount));
    if (result?.new_balance !== undefined) {
      setMessage(`New balance: $${result.new_balance}`);
    } else if (result?.error) {
      setMessage(result.error);
    }
  };

  return (
    <View style={{ flex: 1, padding: 20 }}>
      <Text style={{ fontSize: 24, fontWeight: "bold" }}>Top Up Balance</Text>
      <TextInput
        placeholder="Bank Account ID"
        value={accountId}
        onChangeText={setAccountId}
        style={{ borderWidth: 1, padding: 8, marginVertical: 10 }}
      />
      <TextInput
        placeholder="Amount"
        value={amount}
        onChangeText={setAmount}
        keyboardType="numeric"
        style={{ borderWidth: 1, padding: 8, marginVertical: 10 }}
      />
      <Button title="Transfer" onPress={handleTransfer} />
      {message ? <Text style={{ marginTop: 20 }}>{message}</Text> : null}
    </View>
  );
};

export default TopUpScreen;
