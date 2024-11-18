import { generateQueryHook } from "../api/api";
import { operations } from "../api/schemas";

export const usePrompt = generateQueryHook(
    'prompt',
    generateQueryHook.api.path('/fashiongpt/suggest').method('post'),
);
