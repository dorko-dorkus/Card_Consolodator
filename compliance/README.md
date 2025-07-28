# SAQ A Compliance Overview

This directory contains documentation for maintaining PCI DSS SAQ A scope.

## Scope Summary
- **Cardholder data** is never stored, processed, or transmitted by the application servers.
- All payment processing is handled by our PCI compliant payment service provider (PSP).
- The backend only receives opaque tokens representing cards.

## Key Controls
- HTTPS is enforced for all traffic.
- Web application firewall and rate limiting protect the API.
- User authentication and session management use secure cookies.
- Regular vulnerability scans and patch management procedures are followed.

See [PRIVACY_POLICY.md](../PRIVACY_POLICY.md) and [BREACH_RESPONSE_PLAN.md](../BREACH_RESPONSE_PLAN.md) for additional security and privacy information.

## Removed Features
The application previously included card storage and balance top‑up capabilities. These features have been **removed** to reduce compliance scope. No card numbers or bank account details are persisted.

## Compliance Documents
- [SAQ A Questionnaire](SAQ_A_Questionnaire.pdf)
- [Attestation of Compliance](Attestation_of_Compliance.pdf)
