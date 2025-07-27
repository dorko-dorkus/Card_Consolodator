import React, { useState, useContext } from "react";
import { View, TextInput, Button, StyleSheet } from "react-native";
import { linkBankAccount } from "./api";
import { ThemedText } from "./ThemedText";
import { useColorScheme } from "./hooks/useColorScheme";
import { Colors } from "./constants/Colors";
import { AuthContext } from "./AuthContext";

const BankAccountScreen = () => {
  const { user } = useContext(AuthContext);
  const [bankToken, setBankToken] = useState("");
  const [message, setMessage] = useState("");
  const theme = useColorScheme() ?? "light";
  const tint = Colors[theme].tint;

  const handleLink = async () => {
    if (!user) return;
    const result = await linkBankAccount(user.user_id, bankToken);
    if (result?.message) {
      setMessage(result.message);
    } else if (result?.error) {
      setMessage(result.error);
    }
  };

  return (
    <View style={[styles.container, { backgroundColor: Colors[theme].background }] }>
      <ThemedText style={styles.title}>Link Bank Account</ThemedText>
      <TextInput
        placeholder="Bank token"
        value={bankToken}
        onChangeText={setBankToken}
        style={styles.input}
      />
      <Button color={tint} title="Link Account" onPress={handleLink} />
      {message ? <ThemedText style={styles.message}>{message}</ThemedText> : null}
    </View>
  );
};

export default BankAccountScreen;

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
