import { ActionIcon, Anchor, AppShell, Box, Flex, Group, Text, UnstyledButton } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { IconChevronLeft, IconLayoutDashboard, IconDatabase } from "@tabler/icons-react";
import { useRouter } from "next/router";
import { ReactNode, createContext, useContext, useState } from "react";
import classes from "./app-layout.module.scss";
import { HeaderControl, NavBarControl } from "@/app/app-layout.service";

const Logo = () => (
    <Flex className={classes.logo}>
        <img src="/logo.png" alt="logo" />
    </Flex>
);

interface HeaderContent {
    title: string | ReactNode;
    backAction: (() => void) | null;
}

interface HeaderContextI {
    headerContext: HeaderContent;
    setHeaderContext: (headerContext: HeaderContent) => void;
}

export const HeaderContext = createContext<HeaderContextI>({
    headerContext: {
        title: "Dashboard",
        backAction: null,
    },
    setHeaderContext: () => {},
});

const Header = () => {
    const router = useRouter();
    const {
        headerContext: { title, backAction },
    } = useContext(HeaderContext);

    return (
        <Group className={classes.headerImpl}>
            <Logo />

            {backAction && (
                <ActionIcon variant="transparent" onClick={backAction}>
                    <IconChevronLeft color="#0C111D" />
                </ActionIcon>
            )}
            {typeof title === "string" && title === "Dashboard" ? (
                <Anchor href="/">
                    <Text className={classes.title}></Text>
                </Anchor>
            ) : (
                <Text className={classes.title}>{title}</Text>
            )}
        </Group>
    );
};

const NavBar = () => {
    const navItems = [
        { href: "/", icon: <IconLayoutDashboard color="#667085" size={24} />, label: "Dashboard" },
        { href: "/clothdb", icon: <IconDatabase color="#667085" size={24} />, label: "Clothes Database" },
    ];

    return (
        <>
            {navItems.map((item) => (
                <UnstyledButton key={item.href} component="a" href={item.href} className={classes.navbarButton}>
                    <Group className={classes.navbarButtonGroup}>
                        {item.icon}
                        <div>{item.label}</div>
                    </Group>
                </UnstyledButton>
            ))}
        </>
    );
};

const AppLayout = ({ children }: { children: React.ReactNode }) => {
    const navbarControl = useDisclosure(true);
    const headerControl = useDisclosure(true);
    const [headerContext, setHeaderContext] = useState<HeaderContent>({
        title: "Dashboard",
        backAction: null,
    });

    return (
        <NavBarControl.Provider value={navbarControl}>
            <HeaderContext.Provider value={{ headerContext, setHeaderContext }}>
                <HeaderControl.Provider value={headerControl}>
                    <AppShell
                        header={{ height: 60, collapsed: !headerControl[0] }}
                        navbar={{
                            width: 300,
                            breakpoint: "sm",
                            collapsed: { desktop: !navbarControl[0] },
                        }}
                        padding={0}
                        classNames={classes}
                        className={classes.appShell}
                    >
                        <AppShell.Header>
                            <Header />
                        </AppShell.Header>

                        <AppShell.Navbar p="md">
                            <NavBar />
                        </AppShell.Navbar>

                        <AppShell.Main>{children}</AppShell.Main>
                    </AppShell>
                </HeaderControl.Provider>
            </HeaderContext.Provider>
        </NavBarControl.Provider>
    );
};

export { AppLayout };
export default AppLayout;