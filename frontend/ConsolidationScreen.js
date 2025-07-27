import React, { useState } from "react";
import { View, Button, ActivityIndicator, StyleSheet } from "react-native";
import { consolidateGiftCards } from "./api";
import { ThemedText } from "./ThemedText";
import { useColorScheme } from "./hooks/useColorScheme";
import { Colors } from "./constants/Colors";


const ConsolidationScreen = ({ navigation }) => {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const theme = useColorScheme() ?? "light";
  const tint = Colors[theme].tint;

  const handleConsolidation = async () => {
    setLoading(true);
    const result = await consolidateGiftCards(1);
    setLoading(false);
    if (result?.message) {
      setMessage(result.message);
    }
  };

  return (
    <View style={[styles.container, { backgroundColor: Colors[theme].background }]}>
      <ThemedText style={styles.title}>Consolidate Gift Cards</ThemedText>
      {loading ? <ActivityIndicator size="large" color={tint} /> : null}
      {message ? <ThemedText style={styles.message}>{message}</ThemedText> : null}
      <Button color={tint} title="Consolidate Now" onPress={handleConsolidation} />
      <Button color={tint} title="Go Back" onPress={() => navigation.goBack()} />
    </View>
  );
};

export default ConsolidationScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    alignItems: "center",
    justifyContent: "center",
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 20,
  },
  message: {
    marginTop: 20,
  },
});
