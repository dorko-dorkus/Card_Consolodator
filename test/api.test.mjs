import { test } from 'node:test';
import assert from 'node:assert/strict';
import { fetchGiftCards, consolidateGiftCards } from '../api.js';

test('fetchGiftCards requests correct URL', async () => {
  const userId = 42;
  let calledUrl;
  global.fetch = async (url) => {
    calledUrl = url;
    return { json: async () => ({ ok: true }) };
  };
  const res = await fetchGiftCards(userId);
  assert.strictEqual(calledUrl, `http://your-backend-url/api/gift-cards?user_id=${userId}`);
  assert.deepStrictEqual(res, { ok: true });
});

test('consolidateGiftCards posts correct body', async () => {
  const userId = 5;
  let url, options;
  global.fetch = async (u, opts) => {
    url = u; options = opts;
    return { json: async () => ({ success: true }) };
  };
  const res = await consolidateGiftCards(userId);
  assert.strictEqual(url, 'http://your-backend-url/api/consolidate');
  assert.deepStrictEqual(options, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId })
  });
  assert.deepStrictEqual(res, { success: true });
});
