import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, Button, StyleSheet } from 'react-native';
import { fetchGiftCards, consolidateGiftCards, sessionInfo } from './api';

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
      <Text>Card ID: {item.card_id}</Text>
      <Text>Token: {item.card_token}</Text>
      <Text>Expiry: {item.expiry_date}</Text>
    </View>
  );

  return (
    <View style={styles.container}>
      {loading ? <Text>Loading...</Text> : (
        <FlatList
          data={cards}
          keyExtractor={(item) => item.card_id.toString()}
          renderItem={renderItem}
          ListEmptyComponent={<Text>No gift cards found.</Text>}
        />
      )}
      <Button title="Consolidate Cards" onPress={handleConsolidate} />
      {message ? <Text style={styles.message}>{message}</Text> : null}
    </View>
  );
};

export default GiftCardListScreen;

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  cardItem: { padding: 10, borderBottomWidth: 1, borderColor: '#ccc' },
  message: { marginTop: 10, textAlign: 'center' },
});
