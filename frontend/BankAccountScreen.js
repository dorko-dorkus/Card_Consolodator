import React, { useState } from "react";
import { View, Text, TextInput, Button } from "react-native";
import { linkBankAccount } from "./api";

const BankAccountScreen = () => {
  const [bankToken, setBankToken] = useState("");
  const [message, setMessage] = useState("");

  const handleLink = async () => {
    const result = await linkBankAccount(1, bankToken);
    if (result?.message) {
      setMessage(result.message);
    } else if (result?.error) {
      setMessage(result.error);
    }
  };

  return (
    <View style={{ flex: 1, padding: 20 }}>
      <Text style={{ fontSize: 24, fontWeight: "bold" }}>Link Bank Account</Text>
      <TextInput
        placeholder="Bank token"
        value={bankToken}
        onChangeText={setBankToken}
        style={{ borderWidth: 1, padding: 8, marginVertical: 10 }}
      />
      <Button title="Link Account" onPress={handleLink} />
      {message ? <Text style={{ marginTop: 20 }}>{message}</Text> : null}
    </View>
  );
};

export default BankAccountScreen;
