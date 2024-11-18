import { useContext, useEffect } from "react";
import { HeaderContext } from "../app/app-layout";
import classes from "./dashboard.module.scss";
import { Flex } from "@mantine/core";
import Clothes from "./clothes/clothes";
import Prompt from "./prompt";

const Dashboard = () => {
    const { setHeaderContext } = useContext(HeaderContext);
    useEffect(() => {
        setHeaderContext({
            title: "Dashboard",
            backAction: null,
        });
    }, []);

    return (
        <Flex className={classes.container}>
            <Prompt />
        </Flex>
    );
};

export { Dashboard };
export default Dashboard;