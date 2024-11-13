import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

function EntityList() {
    const [entityType, setEntityType] = useState("trader"); // Default to traders
    const [entities, setEntities] = useState([]);

    useEffect(() => {
        fetch(`/${entityType}s`)
            .then((response) => response.json())
            .then((data) => setEntities(data))
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

            <ul>
                {entities.map((entity) => (
                    <li key={entity.id}>
                        <Link to={`/${entityType}/${entity.id}`}>
                            {entityType === "trader" && entity.name}
                            {entityType === "portfolio" && entity.name}
                            {entityType === "transaction" &&
                                `${entity.stock_code} - ${entity.quantity} shares`}
                        </Link>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default EntityList;
