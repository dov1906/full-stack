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

    if (!portfolio) {
        return <p>Loading...</p>;
    }

    return (
        <div>
            <h2>{portfolio.name}</h2>
            <p>Total Value: ${portfolio.total_value}</p>

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
                        {transaction.stock_code} - {transaction.quantity} shares - ${transaction.stock_price}
                        <br />
                        Date: {new Date(transaction.date).toLocaleDateString()}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default PortfolioDetail;
