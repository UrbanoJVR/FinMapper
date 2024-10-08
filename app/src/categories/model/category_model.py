from database import db


class CategoryModel(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(24), nullable=False, unique=True)
    description = db.Column(db.String(128), nullable=False)
    transactions = db.relationship("TransactionModel", back_populates="category")
