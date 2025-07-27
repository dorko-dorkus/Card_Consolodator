import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from unittest.mock import patch
import stripeUtils


def test_create_payment_intent_calls_stripe():
    with patch('stripeUtils.stripe.PaymentIntent.create') as mock_create:
        mock_create.return_value = {'id': 'pi_123'}
        result = stripeUtils.create_payment_intent(10.5, 1)
        mock_create.assert_called_once_with(
            amount=int(10.5 * 100),
            currency='usd',
            description='Gift Card Consolidation for User 1',
            metadata={'user_id': 1},
        )
        assert result == {'id': 'pi_123'}
