import React, { useState } from "react";
import { View, Text, Button, ActivityIndicator } from "react-native";
import { consolidateGiftCards } from "../api/api";


const ConsolidationScreen = ({ navigation }) => {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleConsolidation = async () => {
    setLoading(true);
    const result = await consolidateGiftCards(1);
    setLoading(false);
    if (result?.message) {
      setMessage(result.message);
    }
  };

  return (
    <View style={{ flex: 1, padding: 20, alignItems: "center" }}>
      <Text style={{ fontSize: 24, fontWeight: "bold" }}>Consolidate Gift Cards</Text>
      {loading ? <ActivityIndicator size="large" color="#0000ff" /> : null}
      {message ? <Text style={{ marginTop: 20 }}>{message}</Text> : null}
      <Button title="Consolidate Now" onPress={handleConsolidation} />
      <Button title="Go Back" onPress={() => navigation.goBack()} />
    </View>
  );
};

export default ConsolidationScreen;
