import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, ActivityIndicator } from 'react-native';
import { COLORS, SPACING, FONT_SIZES } from './theme';
import { loginUser, sessionInfo } from './api';

const LoginScreen = ({ navigation }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    setLoading(true);
    const res = await loginUser(email, password);
    if (res?.error) {
      setMessage(res.error);
    } else {
      const info = await sessionInfo();
      if (info?.authenticated) {
        navigation.replace('Home');
      } else {
        setMessage('Login failed');
      }
    }
    setLoading(false);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Login</Text>
      <TextInput
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        style={styles.input}
      />
      <TextInput
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
        style={styles.input}
      />
      {loading ? (
        <ActivityIndicator size="large" color={COLORS.primary} />
      ) : (
        <Button title="Login" onPress={handleLogin} />
      )}
      {message ? <Text style={styles.message}>{message}</Text> : null}
    </View>
  );
};

export default LoginScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: SPACING,
    justifyContent: 'center',
    backgroundColor: COLORS.background,
  },
  title: {
    fontSize: FONT_SIZES.title,
    fontWeight: 'bold',
    marginBottom: SPACING,
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
