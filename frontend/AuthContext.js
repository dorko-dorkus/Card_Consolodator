import React, { createContext, useState, useEffect } from 'react';
import { getItem, saveItem, deleteItem } from './SecureStore';
import { loginUser, registerUser, logoutUser, sessionInfo } from './api';

export const AuthContext = createContext({
  user: null,
  loading: true,
  login: async () => {},
  register: async () => {},
  logout: async () => {},
});

const STORAGE_KEY = 'auth_user';

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      const stored = await getItem(STORAGE_KEY);
      if (stored) {
        try {
          const parsed = JSON.parse(stored);
          if (parsed && parsed.user_id) {
            setUser(parsed);
          }
        } catch {}
      }
      setLoading(false);
    })();
  }, []);

  const login = async (email, password) => {
    const data = await loginUser(email, password);
    if (!data?.error) {
      let uid = data.user_id;
      if (!uid) {
        const session = await sessionInfo();
        uid = session?.user_id;
      }
      if (uid) {
        const userData = { user_id: uid };
        await saveItem(STORAGE_KEY, JSON.stringify(userData));
        setUser(userData);
      }
    }
    return data;
  };

  const register = async (name, email, password) => {
    const data = await registerUser(name, email, password);
    if (!data?.error && data.user_id) {
      const userData = { user_id: data.user_id };
      await saveItem(STORAGE_KEY, JSON.stringify(userData));
      setUser(userData);
    }
    return data;
  };

  const logout = async () => {
    await logoutUser();
    await deleteItem(STORAGE_KEY);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
