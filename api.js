const API_URL = "http://your-backend-url/api";

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
