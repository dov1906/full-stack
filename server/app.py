#!/usr/bin/env python3

# Remote library imports
from flask import request, make_response, jsonify
from flask_restful import Resource

# Local imports
from config import app, db, api
from models import Trader, Portfolio, Transaction


@app.route("/")
def index():
    return make_response({"message": "Welcome to the Finance Company Management App"}, 200)

class AllTraders(Resource):
    
    def get(self):
        traders = Trader.query.all()
        body = [trader.to_dict(only=("id", "name", "photo")) for trader in traders]
        return make_response(jsonify(body), 200)
    
    def post(self):
        try:
            new_trader = Trader(
                name=request.json.get("name"),
                photo=request.json.get("photo")
            )
            db.session.add(new_trader)
            db.session.commit()
            body = new_trader.to_dict(only=("id", "name", "photo"))
            return make_response(jsonify(body), 201)
        except Exception as e:
            body = {"error": str(e)}
            return make_response(jsonify(body), 400)

api.add_resource(AllTraders, "/traders")
class TraderByID(Resource):

    def get(self, id):
        trader = db.session.get(Trader, id)
        if trader:
            body = trader.to_dict()
            body["portfolios"] = [portfolio.to_dict(only=("id", "name")) for portfolio in trader.portfolios]
            body["transactions"] = [transaction.to_dict() for transaction in trader.transactions]
            return make_response(jsonify(body), 200)
        else:
            return make_response({"error": f"Trader {id} not found."}, 404)

    def delete(self, id):
        trader = db.session.get(Trader, id)
        if trader:
            db.session.delete(trader)
            db.session.commit()
            return make_response({}, 204)
        else:
            return make_response({"error": f"Trader {id} not found."}, 404)

api.add_resource(TraderByID, "/traders/<int:id>")

class AllPortfolios(Resource):
    
    def get(self):
        portfolios = Portfolio.query.all()
        body = [portfolio.to_dict(only=("id", "name")) for portfolio in portfolios]
        return make_response(jsonify(body), 200)
    
    def post(self):
        try:
            new_portfolio = Portfolio(name=request.json.get("name"))
            db.session.add(new_portfolio)
            db.session.commit()
            body = new_portfolio.to_dict(only=("id", "name"))
            return make_response(jsonify(body), 201)
        except Exception as e:
            body = {"error": str(e)}
            return make_response(jsonify(body), 400)

api.add_resource(AllPortfolios, "/portfolios")

class PortfolioByID(Resource):

    def get(self, id):
        portfolio = db.session.get(Portfolio, id)
        if portfolio:
            body = portfolio.to_dict()
            body["traders"] = [trader.to_dict(only=("id", "name")) for trader in portfolio.traders]
            body["transactions"] = [transaction.to_dict() for transaction in portfolio.transactions]
            body["total_value"] = portfolio.total_value
            return make_response(jsonify(body), 200)
        else:
            return make_response({"error": f"Portfolio {id} not found."}, 404)

    def delete(self, id):
        portfolio = db.session.get(Portfolio, id)
        if portfolio:
            db.session.delete(portfolio)
            db.session.commit()
            return make_response({}, 204)
        else:
            return make_response({"error": f"Portfolio {id} not found."}, 404)

api.add_resource(PortfolioByID, "/portfolios/<int:id>")

class AllTransactions(Resource):
    
    def get(self):
        transactions = Transaction.query.all()
        body = [transaction.to_dict() for transaction in transactions]
        return make_response(jsonify(body), 200)
    
    def post(self):
        try:
            new_transaction = Transaction(
                stock_index=request.json.get("stock_index"),
                quantity=request.json.get("quantity"),
                stock_price=request.json.get("stock_price"),
                trader_id=request.json.get("trader_id"),
                portfolio_id=request.json.get("portfolio_id")
            )
            db.session.add(new_transaction)
            db.session.commit()
            body = new_transaction.to_dict()
            return make_response(jsonify(body), 201)
        except Exception as e:
            body = {"error": str(e)}
            return make_response(jsonify(body), 400)

api.add_resource(AllTransactions, "/transactions")

class TransactionByID(Resource):

    def get(self, id):
        transaction = db.session.get(Transaction, id)
        if transaction:
            body = transaction.to_dict()
            return make_response(jsonify(body), 200)
        else:
            return make_response({"error": f"Transaction {id} not found."}, 404)

    def delete(self, id):
        transaction = db.session.get(Transaction, id)
        if transaction:
            db.session.delete(transaction)
            db.session.commit()
            return make_response({}, 204)
        else:
            return make_response({"error": f"Transaction {id} not found."}, 404)

api.add_resource(TransactionByID, "/transactions/<int:id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
