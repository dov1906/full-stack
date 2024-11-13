from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from datetime import datetime
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)



class Trader(db.Model, SerializerMixin):
    __tablename__ = "traders"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    photo = db.Column(db.String, nullable=True)
    
    transactions = db.relationship("Transaction", back_populates="trader", cascade="all")

    @validates("name")
    def validate_name(self, key, value):
        if not value or len(value) < 3:
            raise ValueError("Trader name must be at least 3 characters long.")
        return value

class Portfolio(db.Model, SerializerMixin):
    __tablename__ = "portfolios"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    
    transactions = db.relationship("Transaction", back_populates="portfolio", cascade="all")

    @property
    def total_value(self):
        return sum(t.quantity * t.stock_price for t in self.transactions)

    @validates("name")
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Portfolio name must be provided.")
        return value

class Transaction(db.Model, SerializerMixin):
    __tablename__ = "transactions"
    
    id = db.Column(db.Integer, primary_key=True)
    stock_code = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    stock_price = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    trader_id = db.Column(db.Integer, db.ForeignKey("traders.id"))
    portfolio_id = db.Column(db.Integer, db.ForeignKey("portfolios.id"))

    trader = db.relationship("Trader", back_populates="transactions")
    portfolio = db.relationship("Portfolio", back_populates="transactions")

    serialize_rules = ('-trader.transactions', '-portfolio.transactions')

    @validates("quantity", "stock_price")
    def validate_positive(self, key, value):
        if value <= 0:
            raise ValueError(f"{key.capitalize()} must be a positive value.")
        return value

    @property
    def total_amount(self):
        return self.quantity * self.stock_price

