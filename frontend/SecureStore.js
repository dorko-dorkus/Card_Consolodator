import * as SecureStore from 'expo-secure-store';

export async function saveItem(key, value) {
  try {
    await SecureStore.setItemAsync(key, value);
  } catch (e) {
    console.warn('Failed to save item', e);
  }
}

export async function getItem(key) {
  try {
    return await SecureStore.getItemAsync(key);
  } catch (e) {
    console.warn('Failed to get item', e);
    return null;
  }
}

export async function deleteItem(key) {
  try {
    await SecureStore.deleteItemAsync(key);
  } catch (e) {
    console.warn('Failed to delete item', e);
  }
}
