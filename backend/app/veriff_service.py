import os
import requests
from .config import Config

VERIFF_API_KEY = os.getenv('VERIFF_API_KEY')
VERIFF_BASE_URL = os.getenv('VERIFF_BASE_URL', 'https://api.veriff.me/v1')

class VeriffError(Exception):
    pass

def create_verification_session(user_id: int) -> str:
    """Create a Veriff session and return the session ID."""
    if not VERIFF_API_KEY:
        raise VeriffError('VERIFF_API_KEY not configured')
    payload = {
        'verification': {
            'person': {'id': str(user_id)},
            'document': {'type': 'passport'},
        }
    }
    headers = {
        'X-AUTH-CLIENT': VERIFF_API_KEY,
        'Content-Type': 'application/json',
    }
    resp = requests.post(f'{VERIFF_BASE_URL}/sessions', json=payload, headers=headers, timeout=10)
    if resp.status_code != 201:
        raise VeriffError(f'Session creation failed: {resp.text}')
    data = resp.json()
    return data['verification']['id']


def fetch_verification_status(session_id: str) -> str:
    """Return Veriff session status."""
    if not VERIFF_API_KEY:
        raise VeriffError('VERIFF_API_KEY not configured')
    headers = {
        'X-AUTH-CLIENT': VERIFF_API_KEY,
        'Content-Type': 'application/json',
    }
    resp = requests.get(f'{VERIFF_BASE_URL}/sessions/{session_id}', headers=headers, timeout=10)
    if resp.status_code != 200:
        raise VeriffError(f'Status fetch failed: {resp.text}')
    data = resp.json()
    return data['verification']['status']
