import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, Button, StyleSheet, ActivityIndicator } from 'react-native';
import { fetchGiftCards, consolidateGiftCards, sessionInfo } from './api';
import { COLORS, SPACING, FONT_SIZES } from './theme';

const GiftCardListScreen = () => {
  const [userId, setUserId] = useState(null);
  const [cards, setCards] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const loadCards = async (uid) => {
    setLoading(true);
    const data = await fetchGiftCards(uid);
    setCards(Array.isArray(data) ? data : []);
    setLoading(false);
  };

  useEffect(() => {
    const loadSession = async () => {
      const info = await sessionInfo();
      if (info?.authenticated) {
        setUserId(info.user_id);
        loadCards(info.user_id);
      }
    };
    loadSession();
  }, []);

  const handleConsolidate = async () => {
    if (!userId) return;
    const res = await consolidateGiftCards(userId);
    if (res?.message) {
      setMessage(res.message);
      loadCards(userId);
    } else if (res?.error) {
      setMessage(res.error);
    } else {
      setMessage('Consolidation failed');
    }
  };

  const renderItem = ({ item }) => (
    <View style={styles.cardItem}>
      <Text style={styles.cardText}>Card ID: {item.card_id}</Text>
      <Text style={styles.cardText}>Token: {item.card_token}</Text>
      <Text style={styles.cardText}>Expiry: {item.expiry_date}</Text>
    </View>
  );

  return (
    <View style={styles.container}>
      {loading ? (
        <ActivityIndicator size="large" color={COLORS.primary} />
      ) : (
        <FlatList
          data={cards}
          keyExtractor={(item) => item.card_id.toString()}
          renderItem={renderItem}
          ListEmptyComponent={<Text style={styles.cardText}>No gift cards found.</Text>}
        />
      )}
      <Button title="Consolidate Cards" onPress={handleConsolidate} />
      {message ? <Text style={styles.message}>{message}</Text> : null}
    </View>
  );
};

export default GiftCardListScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: SPACING,
    backgroundColor: COLORS.background,
  },
  cardItem: {
    padding: SPACING / 2,
    borderBottomWidth: 1,
    borderColor: COLORS.border,
  },
  cardText: {
    fontSize: FONT_SIZES.text,
    color: COLORS.text,
  },
  message: {
    marginTop: SPACING,
    textAlign: 'center',
    color: COLORS.text,
  },
});
