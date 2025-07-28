import React, { useEffect, useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';
import { linkBankAccount, sessionInfo } from './api';

const BankLinkScreen = () => {
  const [userId, setUserId] = useState(null);
  const [bankToken, setBankToken] = useState('');
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

  const handleLink = async () => {
    if (!userId || !bankToken) return;
    const res = await linkBankAccount(userId, bankToken);
    if (res?.message) {
      setMessage(res.message);
    } else if (res?.error) {
      setMessage(res.error);
    }
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
      <Button title="Link" onPress={handleLink} />
      {message ? <Text style={styles.message}>{message}</Text> : null}
    </View>
  );
};

export default BankLinkScreen;

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: '#fff' },
  title: { fontSize: 20, marginBottom: 10, textAlign: 'center' },
  input: { borderWidth: 1, borderColor: '#ccc', padding: 8, marginVertical: 10, borderRadius: 6 },
  message: { marginTop: 20, textAlign: 'center' },
});
