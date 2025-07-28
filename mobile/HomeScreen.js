import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, Button } from 'react-native';
import { sessionInfo, logoutUser } from './api';

const HomeScreen = ({ navigation }) => {
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
        <>
          <Text style={styles.text}>Welcome, user {userId}!</Text>
          <Button
            title="View Gift Cards"
            onPress={() => navigation.navigate('GiftCards')}
          />
          <Button
            title="Link Bank Account"
            onPress={() => navigation.navigate('BankLink')}
          />
          <Button
            title="Make Purchase"
            onPress={() => navigation.navigate('Purchase')}
          />
          <Button
            title="Logout"
            onPress={async () => {
              await logoutUser();
              navigation.replace('Login');
            }}
          />
        </>
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
