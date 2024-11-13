from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData

# Database setup
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)

# Initialize the app and its configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initialize extensions with the app
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
CORS(app)

# Import models after `db` initialization to avoid circular imports
from models import Trader, Portfolio, Transaction

@app.route("/")
def index():
    return make_response({"message": "Welcome to the Finance Company Management App"}, 200)

# Traders Resource
class AllTraders(Resource):
    def get(self):
        traders = [trader.to_dict(only=("id", "name", "photo")) for trader in Trader.query.all()]
        return make_response(jsonify(traders), 200)

    def post(self):
        data = request.get_json()
        try:
            new_trader = Trader(
                name=data.get("name"),
                photo=data.get("photo")
            )
            db.session.add(new_trader)
            db.session.commit()
            return make_response(new_trader.to_dict(only=("id", "name", "photo")), 201)
        except Exception as e:
            return make_response({"error": str(e)}, 400)

api.add_resource(AllTraders, "/traders")

class TraderByID(Resource):
    def patch(self, id):
        trader = db.session.get(Trader, id)

        if trader:
            try:
                # Update only the provided attributes
                for attr in request.json:
                    setattr(trader, attr, request.json.get(attr))
                db.session.commit()
                
                # Specify the fields you want to return in the response
                response_body = trader.to_dict(only=("id", "name", "photo"))
                return make_response(response_body, 200)
            except Exception as e:
                response_body = {
                    "error": "Invalid trader data provided!",
                    "details": str(e)
                }
                return make_response(response_body, 422)
        else:
            response_body = {
                "error": "Trader Not Found!"
            }
            return make_response(response_body, 404)

    def delete(self, id):
        trader = db.session.get(Trader, id)

        if trader:
            db.session.delete(trader)
            db.session.commit()
            return make_response({}, 204)
        else:
            response_body = {
                "error": "Trader Not Found!"
            }
            return make_response(response_body, 404)

api.add_resource(TraderByID, '/traders/<int:id>')


class AllPortfolios(Resource):
    def get(self):
        portfolios = [portfolio.to_dict(only=("id", "name")) for portfolio in Portfolio.query.all()]
        return make_response(jsonify(portfolios), 200)

    def post(self):
        data = request.get_json()
        try:
            new_portfolio = Portfolio(name=data.get("name"))
            db.session.add(new_portfolio)
            db.session.commit()
            return make_response(new_portfolio.to_dict(only=("id", "name")), 201)
        except Exception as e:
            return make_response({"error": str(e)}, 400)

api.add_resource(AllPortfolios, "/portfolios")

class PortfolioByID(Resource):
    def get(self, id):
        portfolio = Portfolio.query.get(id)
        if portfolio:
            body = portfolio.to_dict()
            body["traders"] = [trader.to_dict(only=("id", "name")) for trader in portfolio.traders]
            body["transactions"] = [transaction.to_dict() for transaction in portfolio.transactions]
            body["total_value"] = portfolio.total_value
            return make_response(jsonify(body), 200)
        else:
            return make_response({"error": f"Portfolio with id {id} not found."}, 404)

    def delete(self, id):
        portfolio = Portfolio.query.get(id)
        if portfolio:
            db.session.delete(portfolio)
            db.session.commit()
            return make_response({}, 204)
        else:
            return make_response({"error": f"Portfolio with id {id} not found."}, 404)

api.add_resource(PortfolioByID, "/portfolios/<int:id>")


class AllTransactions(Resource):
    def get(self):
        try:
            transactions = [transaction.to_dict() for transaction in Transaction.query.all()]
            return make_response(jsonify(transactions), 200)
        except Exception as e:
            return make_response({"error": "Internal Server Error", "details": str(e)}, 500)

    def post(self):
        data = request.get_json()
        try:
            new_transaction = Transaction(
                stock_code=data.get("stock_code"),
                quantity=data.get("quantity"),
                stock_price=data.get("stock_price"),
                trader_id=data.get("trader_id"),
                portfolio_id=data.get("portfolio_id")
            )
            db.session.add(new_transaction)
            db.session.commit()
            return make_response(new_transaction.to_dict(), 201)
        except Exception as e:
            return make_response({"error": str(e)}, 400)

api.add_resource(AllTransactions, "/transactions")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
