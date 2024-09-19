from decimal import Decimal
from typing import List

from app.src.transactions.domain.transaction import Transaction
from app.src.utils.date_utils import str_to_date


def map_to_entity_list(transactions_from_file) -> List[Transaction]:
    transactions = []

    for tf in transactions_from_file:
        transactions.append(Transaction(
            transaction_date=str_to_date(tf['date']),
            amount=Decimal(tf['amount'].replace(',', '.')),
            concept=tf['concept']
        ))

    return transactions
