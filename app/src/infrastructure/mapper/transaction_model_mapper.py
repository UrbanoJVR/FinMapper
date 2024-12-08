from typing import List, Sequence

from app.src.domain.transaction import Transaction
from app.src.infrastructure.model.transaction_model import TransactionModel


def map_to_model(transaction: Transaction) -> TransactionModel:
    return TransactionModel(
        id=transaction.id,
        date=transaction.transaction_date,
        amount=transaction.amount,
        concept=transaction.concept,
        category_id=transaction.category.id if transaction.category is not None else None
    )


def map_to_domain(transaction_model: TransactionModel) -> Transaction:
    return Transaction(
        id=transaction_model.id,
        transaction_date=transaction_model.date,
        amount=transaction_model.amount,
        concept=transaction_model.concept,
        category=transaction_model.category
    )


def map_to_model_list(transactions: List[Transaction]) -> List[TransactionModel]:
    tm_list: List[TransactionModel] = []

    for transaction in transactions:
        tm_list.append(map_to_model(transaction))

    return tm_list


def map_to_entity_list(transactions_models: Sequence[TransactionModel]) -> List[Transaction]:
    transactions: List[Transaction] = []

    for transaction_model in transactions_models:
        transactions.append(map_to_domain(transaction_model))

    return transactions
