// Allow the backend base URL to be configured via environment variable.
// Defaults to a local development server if not provided.
const API_BASE = process.env.BACKEND_URL || "http://localhost:5000";
const API_URL = `${API_BASE}/api`;

export const fetchGiftCards = async (userId) => {
  try {
    const response = await fetch(`${API_URL}/gift-cards?user_id=${userId}`);
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
    });
    return await response.json();
  } catch (error) {
    console.error("Error consolidating gift cards:", error);
    return null;
  }
};
