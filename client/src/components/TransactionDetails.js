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

    if (!transaction) {
        return <p>Loading...</p>;
    }

    return (
        <div>
            <h2>Transaction Details</h2>
            <p>Stock Code: {transaction.stock_code}</p>
            <p>Quantity: {transaction.quantity}</p>
            <p>Stock Price: ${transaction.stock_price}</p>
            <p>Total Amount: ${transaction.total_amount}</p>
            <p>Date: {new Date(transaction.date).toLocaleDateString()}</p>

            <h3>Associated Trader</h3>
            <p>
                <Link to={`/trader/${transaction.trader.id}`}>{transaction.trader.name}</Link>
            </p>

            <h3>Associated Portfolio</h3>
            <p>
                <Link to={`/portfolio/${transaction.portfolio.id}`}>{transaction.portfolio.name}</Link>
            </p>
        </div>
    );
}

export default TransactionDetail;
