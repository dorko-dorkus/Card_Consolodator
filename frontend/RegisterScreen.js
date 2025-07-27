import React, { useState, useContext } from 'react';
import { View, TextInput, Button, StyleSheet, TouchableOpacity } from 'react-native';
import { ThemedText } from './ThemedText';
import { useColorScheme } from './hooks/useColorScheme';
import { Colors } from './constants/Colors';
import { AuthContext } from './AuthContext';

const RegisterScreen = ({ navigation }) => {
  const { register } = useContext(AuthContext);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const theme = useColorScheme() ?? 'light';
  const tint = Colors[theme].tint;

  const handleRegister = async () => {
    const res = await register(name, email, password);
    if (res?.error) {
      setMessage(res.error);
    }
  };

  return (
    <View style={[styles.container, { backgroundColor: Colors[theme].background }] }>
      <ThemedText style={styles.title}>Register</ThemedText>
      <TextInput placeholder="Name" value={name} onChangeText={setName} style={styles.input} />
      <TextInput placeholder="Email" value={email} onChangeText={setEmail} style={styles.input} />
      <TextInput
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
        style={styles.input}
      />
      <Button color={tint} title="Register" onPress={handleRegister} />
      {message ? <ThemedText style={styles.message}>{message}</ThemedText> : null}
      <TouchableOpacity onPress={() => navigation.navigate('Login')}>
        <ThemedText style={[styles.link, {color: tint}]}>Back to Login</ThemedText>
      </TouchableOpacity>
    </View>
  );
};

export default RegisterScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    justifyContent: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  input: {
    borderWidth: 1,
    padding: 8,
    marginVertical: 10,
    borderRadius: 6,
  },
  message: {
    marginTop: 20,
  },
  link: {
    marginTop: 15,
    textAlign: 'center',
  },
});
