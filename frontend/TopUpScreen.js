import React, { useState, useContext } from "react";
import { View, TextInput, Button, StyleSheet } from "react-native";
import { transferFromBank } from "./api";
import { ThemedText } from "./ThemedText";
import { useColorScheme } from "./hooks/useColorScheme";
import { Colors } from "./constants/Colors";
import { AuthContext } from "./AuthContext";

const TopUpScreen = () => {
  const { user } = useContext(AuthContext);
  const [accountId, setAccountId] = useState("");
  const [amount, setAmount] = useState("");
  const [message, setMessage] = useState("");
  const theme = useColorScheme() ?? "light";
  const tint = Colors[theme].tint;

  const handleTransfer = async () => {
    if (!user) return;
    const result = await transferFromBank(user.user_id, accountId, parseFloat(amount));
    if (result?.new_balance !== undefined) {
      setMessage(`New balance: $${result.new_balance}`);
    } else if (result?.error) {
      setMessage(result.error);
    }
  };

  return (
    <View style={[styles.container, { backgroundColor: Colors[theme].background }] }>
      <ThemedText style={styles.title}>Top Up Balance</ThemedText>
      <TextInput
        placeholder="Bank Account ID"
        value={accountId}
        onChangeText={setAccountId}
        style={styles.input}
      />
      <TextInput
        placeholder="Amount"
        value={amount}
        onChangeText={setAmount}
        keyboardType="numeric"
        style={styles.input}
      />
      <Button color={tint} title="Transfer" onPress={handleTransfer} />
      {message ? <ThemedText style={styles.message}>{message}</ThemedText> : null}
    </View>
  );
};

export default TopUpScreen;

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
