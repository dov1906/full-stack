#!/usr/bin/env python3

from app import app
from models import db, Trader, Portfolio, Transaction
from datetime import datetime, timedelta
import random

with app.app_context():
    # Clear existing data
    Trader.query.delete()
    Portfolio.query.delete()
    Transaction.query.delete()

    print("Starting seed...")

    # Define sample traders with photos
    traders = [
        Trader(name="Elon Musk", photo="https://www.investopedia.com/thmb/7Z5UZm0oBMYNOjVxGi_9iuJFclE=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/GettyImages-1948568886-a2bfa43b20004a6f82c8a0381d196933.jpg"),
        Trader(name="Warren Buffett", photo="https://hips.hearstapps.com/hmg-prod/images/warren_buffett_steve_pope_getty_images_501615406.jpg"),
        Trader(name="Jeff Bezos", photo="https://images.seattletimes.com/wp-content/uploads/2023/11/11032023_1_155400.jpg"),
        Trader(name="Bill Gates", photo="https://imageio.forbes.com/specials-images/imageserve/62d599ede3ff49f348f9b9b4/0x0.jpg?format=jpg&crop=821,821,x155,y340,safe&height=416&width=416&fit=bounds"),
        Trader(name="Amancio Ortega", photo="https://imageio.forbes.com/specials-images/imageserve/5c76b94131358e35dd27748e/0x0.jpg?format=jpg&crop=2053,2053,x179,y216,safe&height=416&width=416&fit=bounds"),
        Trader(name="Mark Zuckerberg", photo="https://imageio.forbes.com/specials-images/imageserve/65458ad4203ccb10402aeab9/US-INTERNET-ADVERTISING-META/0x0.jpg?crop=2064,1376,x0,y0,safe&height=474&width=711&fit=bounds"),
        Trader(name="Ursula von der Leyen", photo="https://www.forbes.fr/wp-content/uploads/2022/12/gettyimages-1150821995.jpg.webp"),
        Trader(name="Abigail Johnson", photo="https://cdn.gobankingrates.com/wp-content/uploads/2022/07/Abigail-Johnson.png?quality=75"),
        Trader(name="Rafaela Aponte-Diamant", photo="https://en.channeliam.com/wp-content/uploads/2024/10/Rafaela-Aponte-Diamant.webp"),
        Trader(name="JK Rowling", photo="https://hips.hearstapps.com/hmg-prod/images/gettyimages-1061157246.jpg"),
        Trader(name="Alice Walton", photo="https://www.financialexpress.com/wp-content/uploads/2024/05/0x0.webp?w=413"),
        Trader(name="Jacob Rothschild", photo="https://bostonglobe-prod.cdn.arcpublishing.com/resizer/v2/FBFKECP57G3JKOZJTTQAOMZQ7Y.jpg"),
        Trader(name="David Solomon", photo="https://fortune.com/wp-content/uploads/2024/07/solomon-070924.jpg"),
        Trader(name="George Soros", photo="https://foreignpolicy.com/wp-content/uploads/2023/09/GettyImages-1240879563-e1694187410161.jpeg"),
        Trader(name="Ray Dalio", photo="https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Ray_Dalio_in_2020.png/440px-Ray_Dalio_in_2020.png"),
        Trader(name="Larry Fink", photo="https://www.fidelity.com/careers/life-at-fidelity/team-spotlight/larry-fink.png")
    ]
    db.session.add_all(traders)

    # Create portfolios with multiple traders associated
    portfolios = [
        Portfolio(name="Growth Portfolio"),
        Portfolio(name="Dividend Portfolio"),
        Portfolio(name="Tech Portfolio"),
        Portfolio(name="Value Portfolio"),
        Portfolio(name="International Portfolio"),
        Portfolio(name="Income Portfolio"),
        Portfolio(name="Aggressive Growth Portfolio")
    ]
    db.session.add_all(portfolios)

    # Assign random traders to portfolios
    for portfolio in portfolios:
        portfolio.traders = random.sample(traders, random.randint(1, 4))

    # Define stock codes for transactions
    stock_codes = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA", "META", "NVDA", "BABA", "JPM", "MA", "ORCL", "XOM", "BAC", "KO", "ADBE", "ABBV" ]

    # Create random transactions
    for _ in range(300):
        trader = random.choice(traders)
        portfolio = random.choice(portfolios)
        stock_code = random.choice(stock_codes)
        quantity = random.randint(1, 100)  # Random quantity between 1 and 100
        stock_price = round(random.uniform(50.0, 500.0), 2)  # Random price between 50 and 500
        transaction_date = datetime.now() - timedelta(days=random.randint(0, 365))  # Random date within the last year

        transaction = Transaction(
            stock_code=stock_code,
            quantity=quantity,
            stock_price=stock_price,
            date=transaction_date,
            trader=trader,
            portfolio=portfolio
        )
        db.session.add(transaction)

    # Commit all records to the database
    db.session.commit()

    print("🌱 Database successfully seeded with Traders, Portfolios, and Transactions! 🌱")
