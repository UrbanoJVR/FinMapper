from app import db


class CategoryModel(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(24), nullable=False)
    description = db.Column(db.String(128), nullable=False)
