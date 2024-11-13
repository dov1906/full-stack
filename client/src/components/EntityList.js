import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";


function EntityList() {
    const [entityType, setEntityType] = useState("trader"); // Default to traders
    const [entities, setEntities] = useState([]);

    useEffect(() => {
        fetch(`/${entityType}s`)
            .then((response) => response.json())
            .then((data) => {
                console.log("Fetched data:", data); // Debug log
                setEntities(data);
            })
            .catch((error) => console.error("Error fetching data:", error));
    }, [entityType]);

    const handleEntityTypeChange = (e) => {
        setEntityType(e.target.value);
    };

    return (
        <div>
            <h1>Entity List</h1>
            <label>Select Entity Type:</label>
            <select value={entityType} onChange={handleEntityTypeChange}>
                <option value="trader">Traders</option>
                <option value="portfolio">Portfolios</option>
                <option value="transaction">Transactions</option>
            </select>

            <ul className={`entity-list ${entityType === "transaction" ? "transactions-view" : ""}`}>
                {entities.map((entity) => (
                    <li key={entity.id} className="entity-card">
                        <Link to={`/${entityType}/${entity.id}`}>
                            {entityType === "trader" && (
                                <>
                                    <img
                                        src={entity.photo}
                                        alt={`${entity.name}`}
                                        className="trader-photo"
                                    />
                                    <p className="entity-name">{entity.name}</p>
                                </>
                            )}
                            {entityType === "portfolio" && (
                                <>
                                    <p className="entity-name">{entity.name}</p>
                                    <p className="entity-total-value">
                                        Total Value: ${entity.total_value || "N/A"}
                                    </p>
                                </>
                            )}
                            {entityType === "transaction" && (
                                <p className="entity-transaction">
                                {entity.stock_code} - {entity.quantity} shares - Price: ${entity.stock_price} - 
                                Date: {new Date(entity.date).toLocaleDateString()} - 
                                Value: ${(entity.quantity * entity.stock_price).toFixed(2)} 
                            </p>
                            )}
                        </Link>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default EntityList;
