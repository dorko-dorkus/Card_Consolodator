const crypto = require('crypto');

/**
 * Tokenize sensitive data on the client so the server only receives
 * opaque values. This simple implementation generates a SHA-256 hash
 * and prefixes it with 'tok_'.
 */
export function tokenize(value) {
  const hash = crypto
    .createHash('sha256')
    .update(String(value))
    .digest('hex');
  return 'tok_' + hash.slice(0, 24);
}
