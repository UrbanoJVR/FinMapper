from app.src.transactions.domain.transaction import Transaction
from app.src.transactions.presentation.forms import TransactionForm


def map_form_to_transaction(form: TransactionForm) -> Transaction:
    return Transaction(
            id=transaction_id,
            transaction_date=form.date.data,
            amount=form.amount.data,
            concept=form.concept.data,
            category=category_service.get_by_id(int(str(form.category.data)))
        )