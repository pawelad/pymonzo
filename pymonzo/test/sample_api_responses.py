# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json


# Source: https://monzo.com/docs/#list-accounts
ACCOUNTS_API_RESPONSE = json.loads('{ \
    "accounts": [ \
        { \
            "id": "acc_00009237aqC8c5umZmrRdh", \
            "description": "Peter Pan\'s Account", \
            "created": "2015-11-13T12:17:42Z" \
        } \
    ] \
}')


# Source: https://monzo.com/docs/#read-balance
BALANCE_API_RESPONSE = json.loads('{ \
    "balance": 5000, \
    "currency": "GBP", \
    "spend_today": 0 \
}')


# Source: https://monzo.com/docs/#retrieve-transaction
TRANSACTION_API_RESPONSE = json.loads('{ \
    "transaction": { \
        "account_balance": 13013, \
        "amount": -510, \
        "created": "2015-08-22T12:20:18Z", \
        "currency": "GBP", \
        "description": "THE DE BEAUVOIR DELI C LONDON        GBR", \
        "id": "tx_00008zIcpb1TB4yeIFXMzx", \
        "merchant": { \
            "address": { \
                "address": "98 Southgate Road", \
                "city": "London", \
                "country": "GB", \
                "latitude": 51.54151, \
                "longitude": -0.08482400000002599, \
                "postcode": "N1 3JD", \
                "region": "Greater London" \
            }, \
            "created": "2015-08-22T12:20:18Z", \
            "group_id": "grp_00008zIcpbBOaAr7TTP3sv", \
            "id": "merch_00008zIcpbAKe8shBxXUtl", \
            "logo": "https://pbs.twimg.com/profile_images/527043602623389696/68_SgUWJ.jpeg", \
            "emoji": "🍞", \
            "name": "The De Beauvoir Deli Co.", \
            "category": "eating_out" \
        }, \
        "metadata": {}, \
        "notes": "Salmon sandwich 🍞", \
        "is_load": false, \
        "settled": "2015-08-23T12:20:18Z" \
    } \
}')
