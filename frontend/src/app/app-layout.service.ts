import { useDisclosure } from "@mantine/hooks";
import { createContext, useContext, useEffect } from "react";

export const NavBarControl = createContext<ReturnType<typeof useDisclosure>>([
    true,
    {
        open: () => { },
        close: () => { },
        toggle: () => { },
    },
]);

export const HeaderControl = createContext<ReturnType<typeof useDisclosure>>([
    true,
    {
        open: () => { },
        close: () => { },
        toggle: () => { },
    },
]);


export const useDisableNavbar = () => {
    const [navbarOpen, { open, close }] = useContext(NavBarControl);

    useEffect(() => () => open(), []);
    useEffect(() => {
        if (navbarOpen) {
            close();
        }
    }, [navbarOpen, close]);
};

export const useDisableHeader = () => {
    const [headerOpen, { open, close }] = useContext(HeaderControl);

    useEffect(() => () => open(), []);
    useEffect(() => {
        if (headerOpen) {
            close();
        }
    }, [headerOpen, close]);
};