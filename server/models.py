from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from datetime import datetime
from config import db

# Association Table for Many-to-Many Relationship between Trader and Portfolio
trader_portfolio = db.Table(
    "trader_portfolio",
    db.Column("trader_id", db.Integer, db.ForeignKey("traders.id"), primary_key=True),
    db.Column("portfolio_id", db.Integer, db.ForeignKey("portfolios.id"), primary_key=True),
    db.Column("role", db.String)  # Optional field, e.g., trader's role in the portfolio
)

# Trader Model
class Trader(db.Model, SerializerMixin):
    __tablename__ = "traders"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    photo = db.Column(db.String, nullable=True)

    # Many-to-many relationship with Portfolio
    portfolios = db.relationship(
        "Portfolio",
        secondary=trader_portfolio,
        back_populates="traders"
    )

    # One-to-many relationship with Transaction
    transactions = db.relationship("Transaction", back_populates="trader", cascade="all")

    # Proxy to access portfolios associated with transactions
    portfolio_associations = association_proxy(
        "transactions", "portfolio", creator=lambda pf: Transaction(portfolio=pf)
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or len(value) < 3:
            raise ValueError("Trader name must be at least 3 characters long.")
        return value

# Portfolio Model
class Portfolio(db.Model, SerializerMixin):
    __tablename__ = "portfolios"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    # Many-to-many relationship with Trader
    traders = db.relationship(
        "Trader",
        secondary=trader_portfolio,
        back_populates="portfolios"
    )

    # One-to-many relationship with Transaction
    transactions = db.relationship("Transaction", back_populates="portfolio", cascade="all")

    # Total value calculation based on transactions
    @property
    def total_value(self):
        return sum(t.quantity * t.stock_price for t in self.transactions)

    @validates("name")
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Portfolio name must be provided.")
        return value

# Transaction Model
class Transaction(db.Model, SerializerMixin):
    __tablename__ = "transactions"
    
    id = db.Column(db.Integer, primary_key=True)
    stock_index = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    stock_price = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Foreign keys for Trader and Portfolio
    trader_id = db.Column(db.Integer, db.ForeignKey("traders.id"))
    portfolio_id = db.Column(db.Integer, db.ForeignKey("portfolios.id"))

    # Relationships
    trader = db.relationship("Trader", back_populates="transactions")
    portfolio = db.relationship("Portfolio", back_populates="transactions")

    @validates("stock_index")
    def validate_stock_index(self, key, value):
        if not isinstance(value, str):
            raise ValueError("Stock index must be a string.")
        return value

    @validates("quantity", "stock_price")
    def validate_positive(self, key, value):
        if value <= 0:
            raise ValueError(f"{key.capitalize()} must be a positive value.")
        return value

    # Calculate the total amount for the transaction
    @property
    def total_amount(self):
        return self.quantity * self.stock_price
