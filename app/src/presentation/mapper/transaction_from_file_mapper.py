from decimal import Decimal
from typing import List

from app.src.domain.transaction.transaction import Transaction
from app.src.domain.transaction.vo.transaction_amount import TransactionAmount
from app.src.domain.transaction.vo.transaction_date import TransactionDate
from app.src.shared.date_utils import str_to_date


def map_to_entity_list(transactions_from_file) -> List[Transaction]:
    transactions = []

    for transaction in transactions_from_file:
        transactions.append(Transaction(
            transaction_date=TransactionDate(str_to_date(transaction['date'])),
            amount=TransactionAmount(Decimal(transaction['amount'].replace(',', '.'))),
            concept=transaction['concept']
        ))

    return transactions
