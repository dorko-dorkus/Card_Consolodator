import React, { useEffect, useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';
import { makePurchase, sessionInfo } from './api';

const PurchaseScreen = () => {
  const [userId, setUserId] = useState(null);
  const [amount, setAmount] = useState('');
  const [paymentToken, setPaymentToken] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const loadSession = async () => {
      const info = await sessionInfo();
      if (info?.authenticated) {
        setUserId(info.user_id);
      }
    };
    loadSession();
  }, []);

  const handlePurchase = async () => {
    if (!userId || !amount || !paymentToken) return;
    const res = await makePurchase(userId, Number(amount), paymentToken);
    if (res?.message) {
      setMessage(res.message);
    } else if (res?.error) {
      setMessage(res.error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Make Purchase</Text>
      <TextInput
        placeholder="Amount"
        value={amount}
        onChangeText={setAmount}
        keyboardType="numeric"
        style={styles.input}
      />
      <TextInput
        placeholder="Payment token"
        value={paymentToken}
        onChangeText={setPaymentToken}
        style={styles.input}
      />
      <Button title="Purchase" onPress={handlePurchase} />
      {message ? <Text style={styles.message}>{message}</Text> : null}
    </View>
  );
};

export default PurchaseScreen;

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: '#fff' },
  title: { fontSize: 20, marginBottom: 10, textAlign: 'center' },
  input: { borderWidth: 1, borderColor: '#ccc', padding: 8, marginVertical: 10, borderRadius: 6 },
  message: { marginTop: 20, textAlign: 'center' },
});
