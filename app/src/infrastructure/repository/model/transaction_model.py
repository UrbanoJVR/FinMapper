from database import db


class TransactionModel(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    concept = db.Column(db.String(100), nullable=False)
    comments = db.Column(db.String(100), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='RESTRICT'), nullable=True)
    category = db.relationship("CategoryModel", back_populates="transactions")
