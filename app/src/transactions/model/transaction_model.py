from app import db


class TransactionModel(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    concept = db.Column(db.String(32), nullable=False)
    category = db.Column(db.String(32), nullable=False)
