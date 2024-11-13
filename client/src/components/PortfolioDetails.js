import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

function PortfolioDetail() {
    const { id } = useParams();
    const [portfolio, setPortfolio] = useState(null);

    useEffect(() => {
        fetch(`/portfolios/${id}`)
            .then((response) => response.json())
            .then((data) => setPortfolio(data))
            .catch((error) => console.error("Error fetching portfolio:", error));
    }, [id]);

    const handleDelete = () => {
        fetch(`/portfolios/${id}`, {
            method: "DELETE",
        })
            .then((response) => {
                if (response.ok) {
                    alert("Portfolio deleted successfully.");
                    setPortfolio(null);
                } else {
                    alert("Failed to delete portfolio.");
                }
            })
            .catch((error) => console.error("Error deleting portfolio:", error));
    };

    if (!portfolio) {
        return <p>Loading...</p>;
    }

    return (
        <div className="portfolio-details">
            <h2>{portfolio.name}</h2>
            <p className="portfolio-total-value">
                Total Value: <span className="portfolio-amount">${portfolio.total_value}</span>
            </p>

            <h3>Associated Traders</h3>
            <ul>
                {portfolio.traders.map((trader) => (
                    <li key={trader.id}>
                        <Link to={`/trader/${trader.id}`}>{trader.name}</Link>
                    </li>
                ))}
            </ul>

            <h3>Transactions</h3>
            <ul>
                {portfolio.transactions.map((transaction) => (
                    <li key={transaction.id}>
                        <strong> {transaction.stock_code} </strong> - {transaction.quantity} shares - ${transaction.stock_price} - <strong>Date:</strong> {new Date(transaction.date).toLocaleDateString()} - <strong>Value:</strong>  {transaction.quantity * transaction.stock_price}
                    </li>
                ))}
            </ul>

            <button className="delete-button" onClick={handleDelete}>
                Delete Portfolio
            </button>
        </div>
    );
}

export default PortfolioDetail;
