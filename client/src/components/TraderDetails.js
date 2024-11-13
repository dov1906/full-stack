import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

function TraderDetail() {
    const { id } = useParams();
    const [trader, setTrader] = useState(null);

    useEffect(() => {
        fetch(`/traders/${id}`)
            .then((response) => response.json())
            .then((data) => setTrader(data))
            .catch((error) => console.error("Error fetching trader:", error));
    }, [id]);

    if (!trader) {
        return <p>Loading...</p>;
    }

    return (
        <div>
            <h2>{trader.name}</h2>
            <img src={trader.photo} alt={`${trader.name}'s photo`} />
            
            <h3>Portfolios</h3>
            <ul>
                {trader.portfolios.map((portfolio) => (
                    <li key={portfolio.id}>
                        <Link to={`/portfolio/${portfolio.id}`}>{portfolio.name}</Link>
                    </li>
                ))}
            </ul>

            <h3>Transactions</h3>
            <ul>
                {trader.transactions.map((transaction) => (
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

export default TraderDetail;
