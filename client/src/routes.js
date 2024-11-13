import React from "react";
import App from "./components/App";
import ErrorPage from "./components/ErrorPage";
import Home from "./components/Home";
import EntityList from "./components/EntityList";
import NewEntityForm from "./components/NewEntityForm";
import Statistics from "./components/Statistics";
import TraderDetail from "./components/TraderDetails";
import PortfolioDetail from "./components/PortfolioDetails";
import TransactionDetail from "./components/TransactionDetails";

const routes = [
    {
        path: "/",
        element: <App />,
        errorElement: <ErrorPage />,
        children: [
            { path: "/", element: <Home /> },
            { path: "/entities", element: <EntityList /> },
            { path: "/add_entity", element: <NewEntityForm /> },
            { path: "/statistics", element: <Statistics /> },
            { path: "/trader/:id", element: <TraderDetail /> },
            { path: "/portfolio/:id", element: <PortfolioDetail /> },
            { path: "/transaction/:id", element: <TransactionDetail /> },
        ],
    },
];

export default routes;
