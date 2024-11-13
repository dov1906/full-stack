#!/usr/bin/env python3

from app import app
from models import db, Trader, Portfolio, Transaction

with app.app_context():
    # Clear existing data
    Trader.query.delete()
    Portfolio.query.delete()
    Transaction.query.delete()

    print("Starting seed...")

    # Create a sample Trader
    trader1 = Trader(
        name="John Doe",
        photo="./images/john_doe.jpg"
    )

    # Create a sample Portfolio
    portfolio1 = Portfolio(
        name="Growth Portfolio"
    )

    # Create a sample Transaction
    transaction1 = Transaction(
        stock_code="AAPL",
        quantity=10,
        stock_price=150.0,
        trader=trader1,  # Associate directly with the trader
        portfolio=portfolio1  # Associate directly with the portfolio
    )

    # Add all records to the session
    db.session.add_all([trader1, portfolio1, transaction1])
    db.session.commit()

    print("🌱 Database successfully seeded with Trader, Portfolio, Transaction! 🌱")
