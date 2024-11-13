import React from "react";
import App from "./components/App";
import ErrorPage from "./components/ErrorPage";
import Home from "./components/Home";
import EntityList from "./components/EntityList";
import NewEntityForm from "./components/NewEntityForm";
import Statistics from "./components/Statistics";

const routes = [
    {
        path: "/",
        element: <App />,
        errorElement: <ErrorPage />,
        children: [
            {
                path: "/",
                element: <Home />,
            },
            {
                path: "/entities",
                element: <EntityList />,
            },
            {
                path: "/add_entity",
                element: <NewEntityForm />,
            },
            {
                path: "/statistics",
                element: <Statistics />,
            },
        ],
    },
];

export default routes;
