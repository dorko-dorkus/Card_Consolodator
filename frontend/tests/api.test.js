process.env.BACKEND_URL = 'http://your-backend-url';
const {fetchGiftCards, consolidateGiftCards} = require('../api');

global.fetch = jest.fn();

afterEach(() => {
  jest.resetAllMocks();
});

test('fetchGiftCards makes request to correct URL', async () => {
  fetch.mockResolvedValue({json: () => Promise.resolve([{card_id:1}])});
  const data = await fetchGiftCards(1);
  expect(fetch).toHaveBeenCalledWith('http://your-backend-url/api/gift-cards?user_id=1');
  expect(data).toEqual([{card_id:1}]);
});

test('consolidateGiftCards posts data', async () => {
  fetch.mockResolvedValue({json: () => Promise.resolve({message:'ok'})});
  const data = await consolidateGiftCards(2);
  expect(fetch).toHaveBeenCalledWith('http://your-backend-url/api/consolidate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: 2 }),
  });
  expect(data).toEqual({message:'ok'});
});
