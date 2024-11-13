import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

function TransactionDetail() {
    const { id } = useParams();
    const [transaction, setTransaction] = useState(null);

    useEffect(() => {
        fetch(`/transactions/${id}`)
            .then((response) => response.json())
            .then((data) => setTransaction(data))
            .catch((error) => console.error("Error fetching transaction:", error));
    }, [id]);

    const handleDelete = () => {
        fetch(`/transactions/${id}`, {
            method: "DELETE",
        })
            .then((response) => {
                if (response.ok) {
                    alert("Transaction deleted successfully.");
                    setTransaction(null);
                } else {
                    alert("Failed to delete transaction.");
                }
            })
            .catch((error) => console.error("Error deleting transaction:", error));
    };

    if (!transaction) {
        return <p>Loading...</p>;
    }

    return (
        <div className="transaction-details">
            <h2>Transaction Details</h2>
            <p className="transaction-info">Stock Code: {transaction.stock_code}</p>
            <p className="transaction-info">Quantity: {transaction.quantity} shares</p>
            <p className="transaction-info">Price: ${transaction.stock_price}</p>
            <p className="transaction-info">Total Value: ${(transaction.quantity * transaction.stock_price).toFixed(2)}</p>
            <p className="transaction-info">Date: {new Date(transaction.date).toLocaleDateString()}</p>

            <h3>Associated Trader</h3>
            <p>
                <Link to={`/trader/${transaction.trader.id}`}>
                    {transaction.trader.name}
                </Link>
            </p>

            <h3>Associated Portfolio</h3>
            <p>
                <Link to={`/portfolio/${transaction.portfolio.id}`}>
                    {transaction.portfolio.name}
                </Link>
            </p>

            <button className="delete-button" onClick={handleDelete}>Delete Transaction</button>
        </div>
    );
}

export default TransactionDetail;
