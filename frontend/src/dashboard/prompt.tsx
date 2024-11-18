import { Button, Flex, Textarea, Text, Paper } from "@mantine/core";
import { useState } from "react";
import { usePrompt } from "./prompt.query";
import ReactMarkdown from 'react-markdown';

const Prompt = () => {
    const [prompt, setPrompt] = useState("");
    const [suggestions, setSuggestions] = useState<string | null>(null);

    const handleSubmit = async () => {
        try {
            const response = await usePrompt.apiCall({ prompt });
            setSuggestions(response?.data?.suggestion ?? null);
        } catch (error) {
            console.error("Error getting suggestions:", error);
        }
    };

    return (
        <Paper p="md" radius="md" withBorder>
            <Flex direction="column" gap="md">
                <Text>
                    Ask for Outfit Suggestions
                </Text>
                <Textarea
                    value={prompt}
                    onChange={(e) => setPrompt(e.currentTarget.value)}
                    placeholder="E.g., Suggest an outfit for a casual dinner"
                    minRows={3}
                />
                <Button 
                    onClick={handleSubmit} 
                    disabled={!prompt.trim()}
                >
                    Get Suggestions
                </Button>
                {suggestions && (
                    <Paper p="sm" withBorder>
                        <ReactMarkdown>{suggestions}</ReactMarkdown>
                    </Paper>
                )}
            </Flex>
        </Paper>
    );
};

export default Prompt; 