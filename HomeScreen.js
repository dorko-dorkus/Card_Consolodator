import React, { useEffect, useState } from "react";
import { View, Text, Button, FlatList } from "react-native";
import { fetchGiftCards, consolidateGiftCards } from "../api/api";

const HomeScreen = ({ navigation }) => {
  const [giftCards, setGiftCards] = useState([]);

  useEffect(() => {
    const loadGiftCards = async () => {
      const data = await fetchGiftCards(1); // Assume user_id = 1
      setGiftCards(data);
    };
    loadGiftCards();
  }, []);

  return (
    <View style={{ flex: 1, padding: 20 }}>
      <Text style={{ fontSize: 24, fontWeight: "bold" }}>Your Gift Cards</Text>
      <FlatList
        data={giftCards}
        keyExtractor={(item) => item.card_id.toString()}
        renderItem={({ item }) => (
          <View style={{ padding: 10, borderBottomWidth: 1 }}>
            <Text>Card Number: {item.card_number}</Text>
            <Text>Balance: ${item.balance.toFixed(2)}</Text>
          </View>
        )}
      />
      <Button title="Consolidate" onPress={() => navigation.navigate("Consolidate")} />
    </View>
  );
};

export default HomeScreen;
