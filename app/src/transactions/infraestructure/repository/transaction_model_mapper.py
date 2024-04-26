from typing import List

from app.src.transactions.domain.transaction import Transaction
from app.src.transactions.model.transaction_model import TransactionModel


def map_to_model(transaction: Transaction) -> TransactionModel:
    return TransactionModel(
        id=transaction.id,
        date=transaction.transaction_date,
        amount=transaction.amount,
        concept=transaction.concept,
        category_id=transaction.category.id if transaction.category is not None else None
    )


def map_to_model_list(transactions: List[Transaction]) -> List[TransactionModel]:
    tm_list: List[TransactionModel] = []

    for transaction in transactions:
        tm_list.append(map_to_model(transaction))

    return tm_list
