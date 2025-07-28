// Allow the backend base URL to be configured via environment variable.
// Defaults to a local development server if not provided.
const API_BASE = process.env.BACKEND_URL || "http://localhost:5000";
const API_URL = `${API_BASE}/api`;

export const fetchGiftCards = async (userId) => {
  try {
    const response = await fetch(`${API_URL}/gift-cards?user_id=${userId}`, {
      credentials: 'include',
    });
    return await response.json();
  } catch (error) {
    console.error("Error fetching gift cards:", error);
    return [];
  }
};

export const consolidateGiftCards = async (userId) => {
  try {
    const response = await fetch(`${API_URL}/consolidate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId }),
      credentials: 'include',
    });
    return await response.json();
  } catch (error) {
    console.error("Error consolidating gift cards:", error);
    return { error: "network_error" };
  }
};

export const linkBankAccount = async (userId, bankToken) => {
  try {
    const response = await fetch(`${API_URL}/bank-accounts/link`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, bank_token: bankToken }),
      credentials: 'include',
    });
    return await response.json();
  } catch (error) {
    console.error("Error linking bank account:", error);
    return { error: "network_error" };
  }
};


export const makePurchase = async (userId, amount, paymentToken) => {
  try {
    const body = { user_id: userId, amount };
    if (paymentToken) {
      body.payment_token = paymentToken;
    }
    const response = await fetch(`${API_URL}/purchase`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      credentials: 'include',
    });
    return await response.json();
  } catch (error) {
    console.error("Error making purchase:", error);
    return { error: "network_error" };
  }
};

export const registerUser = async (name, email, password) => {
  try {
    const response = await fetch(`${API_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password }),
      credentials: 'include',
    });
    return await response.json();
  } catch (error) {
    console.error('Error registering:', error);
    return { error: 'network_error' };
  }
};

export const loginUser = async (email, password) => {
  try {
    const response = await fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
      credentials: 'include',
    });
    return await response.json();
  } catch (error) {
    console.error('Error logging in:', error);
    return { error: 'network_error' };
  }
};

export const logoutUser = async () => {
  try {
    await fetch(`${API_URL}/logout`, { method: 'POST', credentials: 'include' });
  } catch (error) {
    console.error('Error logging out:', error);
  }
};

export const sessionInfo = async () => {
  try {
    const res = await fetch(`${API_URL}/session`, { credentials: 'include' });
    return await res.json();
  } catch (error) {
    console.error('Error fetching session:', error);
    return null;
  }
};

export const deleteAccount = async (userId) => {
  try {
    const res = await fetch(`${API_URL}/users/${userId}`, {
      method: 'DELETE',
      credentials: 'include',
    });
    return await res.json();
  } catch (error) {
    console.error('Error deleting account:', error);
    return null;
  }
};
