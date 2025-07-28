import React, { useEffect, useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, ActivityIndicator } from 'react-native';
import { linkBankAccount, sessionInfo } from './api';
import { COLORS, SPACING, FONT_SIZES } from './theme';

const BankLinkScreen = () => {
  const [userId, setUserId] = useState(null);
  const [bankToken, setBankToken] = useState('');
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

  const handleLink = async () => {
    if (!userId) return;
    if (!bankToken) {
      setMessage('Enter bank token');
      return;
    }
    setLoading(true);
    const res = await linkBankAccount(userId, bankToken);
    if (res?.message) {
      setMessage(res.message);
    } else if (res?.error) {
      setMessage(res.error);
    }
    setLoading(false);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Link Bank Account</Text>
      <TextInput
        placeholder="Bank token"
        value={bankToken}
        onChangeText={setBankToken}
        style={styles.input}
      />
      {loading ? (
        <ActivityIndicator size="large" color={COLORS.primary} />
      ) : (
        <Button title="Link" onPress={handleLink} />
      )}
      {message ? <Text style={styles.message}>{message}</Text> : null}
    </View>
  );
};

export default BankLinkScreen;

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
