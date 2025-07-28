const crypto = require('crypto');

/**
 * Tokenize sensitive data on the client so the server only receives
 * opaque values. A small HMAC helper is used to combine a secret (or
 * per-token random salt) with the data prior to hashing. This keeps
 * tokens stable when a secret is provided while ensuring they remain
 * unpredictable without it.
 */
const TOKENIZER_SECRET = process.env.TOKENIZER_SECRET;

export function tokenize(value) {
  const salt = crypto.randomBytes(16).toString('hex');
  const key = TOKENIZER_SECRET || salt;
  const hash = crypto
    .createHmac('sha256', key)
    .update(String(value) + salt)
    .digest('hex');
  return 'tok_' + hash.slice(0, 24);
}
