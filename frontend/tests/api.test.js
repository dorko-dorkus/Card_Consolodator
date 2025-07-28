process.env.BACKEND_URL = 'http://your-backend-url';
const {fetchGiftCards, consolidateGiftCards, linkBankAccount, makePurchase, deleteAccount} = require('../api');

global.fetch = jest.fn();

afterEach(() => {
  jest.resetAllMocks();
});

test('fetchGiftCards makes request to correct URL', async () => {
  fetch.mockResolvedValue({json: () => Promise.resolve([{card_id:1}])});
  const data = await fetchGiftCards(1);
  expect(fetch).toHaveBeenCalledWith('http://your-backend-url/api/gift-cards?user_id=1', { credentials: 'include' });
  expect(data).toEqual([{card_id:1}]);
});

test('consolidateGiftCards posts data', async () => {
  fetch.mockResolvedValue({json: () => Promise.resolve({message:'ok'})});
  const data = await consolidateGiftCards(2);
  expect(fetch).toHaveBeenCalledWith('http://your-backend-url/api/consolidate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: 2 }),
    credentials: 'include',
  });
  expect(data).toEqual({message:'ok'});
});

test('linkBankAccount posts data', async () => {
  fetch.mockResolvedValue({json: () => Promise.resolve({message:'linked'})});
  const data = await linkBankAccount(1, 'tok_bank');
  expect(fetch).toHaveBeenCalledWith('http://your-backend-url/api/bank-accounts/link', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: 1, bank_token: 'tok_bank' }),
    credentials: 'include',
  });
  expect(data).toEqual({message:'linked'});
});


test('makePurchase posts data', async () => {
  fetch.mockResolvedValue({json: () => Promise.resolve({message:'purchase successful'})});
  const data = await makePurchase(1, 5, 'pm_tok');
  expect(fetch).toHaveBeenCalledWith('http://your-backend-url/api/purchase', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: 1, amount: 5, payment_token: 'pm_tok' }),
    credentials: 'include',
  });
  expect(data).toEqual({message:'purchase successful'});
});

test('deleteAccount sends delete', async () => {
  fetch.mockResolvedValue({json: () => Promise.resolve({message:'account deleted'})});
  const data = await deleteAccount(3);
  expect(fetch).toHaveBeenCalledWith('http://your-backend-url/api/users/3', {
    method: 'DELETE',
    credentials: 'include',
  });
  expect(data).toEqual({message:'account deleted'});
});
