import React, { useEffect, useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, ActivityIndicator } from 'react-native';
import { makePurchase, sessionInfo } from './api';
import { COLORS, SPACING, FONT_SIZES } from './theme';

const PurchaseScreen = () => {
  const [userId, setUserId] = useState(null);
  const [amount, setAmount] = useState('');
  const [paymentToken, setPaymentToken] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

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
    if (!userId || !paymentToken) return;
    const amt = Number(amount);
    if (!amount || isNaN(amt) || amt <= 0) {
      setMessage('Enter a valid amount');
      return;
    }
    setLoading(true);
    const res = await makePurchase(userId, amt, paymentToken);
    if (res?.message) {
      setMessage(res.message);
    } else if (res?.error) {
      setMessage(res.error);
    }
    setLoading(false);
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
      {loading ? (
        <ActivityIndicator size="large" color={COLORS.primary} />
      ) : (
        <Button title="Purchase" onPress={handlePurchase} />
      )}
      {message ? <Text style={styles.message}>{message}</Text> : null}
    </View>
  );
};

export default PurchaseScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: SPACING,
    backgroundColor: COLORS.background,
  },
  title: {
    fontSize: FONT_SIZES.title,
    marginBottom: SPACING / 2,
    textAlign: 'center',
    color: COLORS.text,
  },
  input: {
    borderWidth: 1,
    borderColor: COLORS.border,
    padding: SPACING / 2,
    marginVertical: SPACING / 2,
    borderRadius: 6,
  },
  message: {
    marginTop: SPACING,
    textAlign: 'center',
    color: COLORS.text,
  },
});
