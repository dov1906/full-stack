import React, { useEffect, useState } from "react";
import { useFormik } from "formik";

function NewEntityForm() {
    const [entityType, setEntityType] = useState("trader"); // Default to "trader"
    const [traders, setTraders] = useState([]);
    const [portfolios, setPortfolios] = useState([]);

    useEffect(() => {
        // Fetch traders and portfolios for dropdowns
        fetch("/traders")
            .then((res) => res.json())
            .then((data) => setTraders(data));
        fetch("/portfolios")
            .then((res) => res.json())
            .then((data) => setPortfolios(data));
    }, []);

    const formik = useFormik({
        initialValues: {
            name: "",
            photo: "",
            stock_code: "",
            quantity: "",
            stock_price: "",
            associatedTraders: [], // Updated to be an array for multiple traders
            associatedPortfolio: "",
        },
        onSubmit: (values) => {
            const url = `/${entityType}s`;
            const payload = {
                name: values.name,
                photo: values.photo,
                stock_code: values.stock_code,
                quantity: values.quantity,
                stock_price: values.stock_price,
                trader_ids: values.associatedTraders, // Updated to send an array of trader IDs
                portfolio_id: values.associatedPortfolio,
            };

            fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(payload),
            })
                .then((res) => res.json())
                .then((data) => {
                    alert(`${entityType} added successfully!`);
                    formik.resetForm();
                })
                .catch((error) => console.error("Error adding entity:", error));
        },
    });

    return (
        <div>
            <h2>Add a New {entityType.charAt(0).toUpperCase() + entityType.slice(1)}</h2>
            <label>
                Select Entity Type:
                <select onChange={(e) => setEntityType(e.target.value)} value={entityType}>
                    <option value="trader">Trader</option>
                    <option value="portfolio">Portfolio</option>
                    <option value="transaction">Transaction</option>
                </select>
            </label>

            <form onSubmit={formik.handleSubmit}>
                {entityType === "trader" && (
                    <>
                        <label>
                            Name:
                            <input
                                type="text"
                                name="name"
                                onChange={formik.handleChange}
                                value={formik.values.name}
                            />
                        </label>
                        <label>
                            Photo URL:
                            <input
                                type="text"
                                name="photo"
                                onChange={formik.handleChange}
                                value={formik.values.photo}
                            />
                        </label>
                    </>
                )}

                {entityType === "portfolio" && (
                    <>
                        <label>
                            Name:
                            <input
                                type="text"
                                name="name"
                                onChange={formik.handleChange}
                                value={formik.values.name}
                            />
                        </label>
                    </>
                )}

                {entityType === "transaction" && (
                    <>
                        <label>
                            Stock Code:
                            <input
                                type="text"
                                name="stock_code"
                                onChange={formik.handleChange}
                                value={formik.values.stock_code}
                            />
                        </label>
                        <label>
                            Quantity:
                            <input
                                type="number"
                                name="quantity"
                                onChange={formik.handleChange}
                                value={formik.values.quantity}
                            />
                        </label>
                        <label>
                            Stock Price:
                            <input
                                type="number"
                                name="stock_price"
                                onChange={formik.handleChange}
                                value={formik.values.stock_price}
                            />
                        </label>
                    </>
                )}

                {(entityType === "portfolio" || entityType === "transaction") && (
                    <label>
                        Select Associated Traders:
                        <select
                            name="associatedTraders"
                            onChange={(e) =>
                                formik.setFieldValue(
                                    "associatedTraders",
                                    Array.from(e.target.selectedOptions, option => option.value)
                                )
                            }
                            multiple // Allows multiple selection
                            value={formik.values.associatedTraders}
                        >
                            {traders.map((trader) => (
                                <option key={trader.id} value={trader.id}>
                                    {trader.name}
                                </option>
                            ))}
                        </select>
                    </label>
                )}

                {entityType === "transaction" && (
                    <label>
                        Select Associated Portfolio:
                        <select
                            name="associatedPortfolio"
                            onChange={formik.handleChange}
                            value={formik.values.associatedPortfolio}
                        >
                            <option value="">-- Select Portfolio --</option>
                            {portfolios.map((portfolio) => (
                                <option key={portfolio.id} value={portfolio.id}>
                                    {portfolio.name}
                                </option>
                            ))}
                        </select>
                    </label>
                )}

                <button type="submit">Add {entityType.charAt(0).toUpperCase() + entityType.slice(1)}</button>
            </form>
        </div>
    );
}

export default NewEntityForm;
