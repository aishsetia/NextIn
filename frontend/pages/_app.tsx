// Import styles of packages that you've installed.
// All packages except `@mantine/hooks` require styles imports
import "@mantine/core/styles.css";
import "@mantine/notifications/styles.css";

import AppLayout from "@/app/app-layout";
import "@/styles/globals.css";
import { MantineProvider, createTheme } from "@mantine/core";
import { Notifications } from "@mantine/notifications";
import type { AppProps } from "next/app";
import Head from "next/head";
import { useState } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const theme = createTheme({
    /** Put your mantine theme override here */
});

function App({ Component, pageProps }: AppProps) {
    const [queryClient] = useState(() => new QueryClient());

    return (
        <MantineProvider theme={theme}>
            <Notifications />
            <Head>
                <link rel="preconnect" href="https://fonts.googleapis.com" />
                <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
                <link
                    href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap"
                    rel="stylesheet"
                />
                <title>NextIn</title>
            </Head>
            <QueryClientProvider client={queryClient}>
                <AppLayout>
                    <Component {...pageProps} />
                </AppLayout>
            </QueryClientProvider>
        </MantineProvider>
    );
};

export default App;