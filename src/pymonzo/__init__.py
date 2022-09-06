"""
An - dare I say it - awesome Python Monzo public API wrapper.

Implemented API endpoints:
- [x] GET /ping/whoami
- [x] GET /accounts
- [x] GET /balance
- [x] GET /pots
- [x] PUT /pots/$pot_id/deposit
- [x] PUT /pots/$pot_id/withdraw
- [x] GET /transactions
- [x] GET /transactions/$transaction_id
- [x] PATCH /transactions/$transaction_id
- [x] POST /feed
- [x] POST /attachment/upload
- [x] POST /attachment/register
- [ ] POST /attachment/deregister
- [ ] GET /transaction-receipts
- [ ] PUT /transaction-receipts
- [ ] DELETE /transaction-receipts
- [ ] GET /webhooks
- [ ] POST /webhooks
- [ ] DELETE /webhooks/$webhook_id
"""
from pymonzo.client import MonzoAPI  # noqa

__title__ = "pymonzo"
__version__ = "0.22.0.dev0"
__author__ = "Paweł Adamczak"
__email__ = "pawel.ad@gmail.com"
__url__ = "https://github.com/pawelad/pymonzo"
