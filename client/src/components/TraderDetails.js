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

    const handleDelete = () => {
        fetch(`/traders/${id}`, {
            method: "DELETE",
        })
            .then((response) => {
                if (response.ok) {
                    alert("Trader deleted successfully.");
                    setTrader(null); 
                } else {
                    alert("Failed to delete trader.");
                }
            })
            .catch((error) => console.error("Error deleting trader:", error));
    };

    if (!trader) {
        return <p>Loading...</p>;
    }

    return (
        <div className="trader-details">
            <h2>{trader.name}</h2>
            <img src={trader.photo} alt={`${trader.name}'s photo`} className="trader-photo-large" />
            
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
                    <strong> {transaction.stock_code} </strong> - {transaction.quantity} shares - ${transaction.stock_price} - <strong>Date:</strong> {new Date(transaction.date).toLocaleDateString()} - <strong>Value:</strong>  {transaction.quantity * transaction.stock_price}
                </li>
                ))}
            </ul>

            <button onClick={handleDelete} className="delete-button">Delete Trader</button>
        </div>
    );
}

export default TraderDetail;
