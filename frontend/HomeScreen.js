import React, { useEffect, useState, useContext } from "react";
import { View, Button, FlatList, StyleSheet } from "react-native";
import { fetchGiftCards } from "./api";
import { ThemedText } from "./ThemedText";
import { useColorScheme } from "./hooks/useColorScheme";
import { Colors } from "./constants/Colors";
import { AuthContext } from "./AuthContext";

const HomeScreen = ({ navigation }) => {
  const { user, logout } = useContext(AuthContext);
  const [giftCards, setGiftCards] = useState([]);
  const theme = useColorScheme() ?? "light";
  const tint = Colors[theme].tint;

  useEffect(() => {
    const loadGiftCards = async () => {
      if (!user) return;
      const data = await fetchGiftCards(user.user_id);
      setGiftCards(Array.isArray(data) ? data : []);
    };
    loadGiftCards();
  }, [user]);

  return (
    <View style={[styles.container, { backgroundColor: Colors[theme].background }]}>
      <ThemedText style={styles.title}>Your Gift Cards</ThemedText>
      <ThemedText style={styles.subtitle}>
        Total cards: {giftCards.length}
      </ThemedText>
      <FlatList
        data={giftCards}
        keyExtractor={(item) => item.card_id.toString()}
        renderItem={({ item }) => (
          <View
            style={[
              styles.cardItem,
              { backgroundColor: theme === "light" ? "#fff" : "#1e1e1e" },
            ]}
          >
            <ThemedText>Token: {item.card_token}</ThemedText>
            {item.expiry_date && (
              <ThemedText>Expires: {item.expiry_date}</ThemedText>
            )}
          </View>
        )}
      />
      <Button
        color={tint}
        title="Consolidate"
        onPress={() => navigation.navigate("Consolidate")}
      />
      <Button
        color={tint}
        title="Bank Accounts"
        onPress={() => navigation.navigate("BankAccounts")}
      />
      <Button
        color={tint}
        title="Purchase"
        onPress={() => navigation.navigate("Purchase")}
      />
      <Button color={tint} title="Logout" onPress={logout} />
    </View>
  );
};

export default HomeScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 10,
  },
  cardItem: {
    padding: 15,
    borderRadius: 8,
    marginBottom: 12,
    shadowColor: "#000",
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  subtitle: {
    marginBottom: 8,
  },
});
