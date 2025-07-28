import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { sessionInfo } from './api';

const HomeScreen = () => {
  const [userId, setUserId] = useState(null);

  useEffect(() => {
    const loadSession = async () => {
      const info = await sessionInfo();
      if (info?.authenticated) {
        setUserId(info.user_id);
      }
    };
    loadSession();
  }, []);

  return (
    <View style={styles.container}>
      {userId ? (
        <Text style={styles.text}>Welcome, user {userId}!</Text>
      ) : (
        <Text style={styles.text}>Loading...</Text>
      )}
    </View>
  );
};

export default HomeScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#fff',
  },
  text: {
    fontSize: 18,
  },
});
