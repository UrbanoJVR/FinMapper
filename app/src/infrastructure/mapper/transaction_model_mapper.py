from typing import List, Sequence

from app.src.domain.transaction.transaction import Transaction
from app.src.domain.transaction.vo.transaction_date import TransactionDate
from app.src.infrastructure.mapper.category_model_mapper import CategoryModelMapper
from app.src.infrastructure.repository.model.transaction_model import TransactionModel


def map_to_model(transaction: Transaction) -> TransactionModel:
    return TransactionModel(
        id=transaction.id,
        date=transaction.transaction_date.value,
        amount=transaction.amount,
        concept=transaction.concept,
        comments=transaction.comments,
        category_id=transaction.category.id if transaction.category is not None else None
    )


def map_to_domain(transaction_model: TransactionModel) -> Transaction:
    return Transaction(
        id=transaction_model.id,
        transaction_date=TransactionDate(transaction_model.date),
        amount=transaction_model.amount,
        concept=transaction_model.concept,
        comments=transaction_model.comments,
        category=CategoryModelMapper.map_to_domain(
            transaction_model.category) if transaction_model.category is not None else None
    )


def map_to_model_list(transactions: List[Transaction]) -> List[TransactionModel]:
    tm_list: List[TransactionModel] = []

    for transaction in transactions:
        tm_list.append(map_to_model(transaction))

    return tm_list


def map_to_domain_list(transactions_models: Sequence[TransactionModel]) -> List[Transaction]:
    transactions: List[Transaction] = []

    for transaction_model in transactions_models:
        transactions.append(map_to_domain(transaction_model))

    return transactions
