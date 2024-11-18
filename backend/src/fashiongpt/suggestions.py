from .core.llm import LLMOpenAI

RAW_PROMPT = """
You are an expert consultant specializing in fashion. Your task is to analyze the given prompt and the descriptions of clothing items available with the user, and suggest a combination of clothing items to create a complete outfit.
You should write your response in an advisory manner to the user.

### Prompt:
--PROMPT-START--
{prompt}
--PROMPT-END--

### Clothing Items:
--CLOTHING-ITEMS-START--
{clothing_items}
--CLOTHING-ITEMS-END--

### Instructions:
{output_attributes_description}
"""

OUTPUT_ATTRIBUTES_DESCRIPTION = """
1. **Comprehension:** Carefully read and understand the entire prompt above.
2. **Identification:** Identify all sections and requirements that are crucial for ideating the outfit.
3. **Extraction:** From these sections, extract attributes of clothing items that are relevant to the prompt.
4. **Matching:** Match the extracted attributes with the clothing items available with the user.
5. **Completion:** Find the best combination of clothing items that are relevant to the prompt, that would yield a complete outfit. This should include all items one would need to wear from top to bottom.
6. **Tone:** The tone of your response should be advisory and helpful. You should directly address the user, and abstract away the complexity of the task as well as analysis steps.
"""


def process_prompt(prompt: str, clothing_items: str) -> list[str]:
    model = "gpt-4o"
    messages = [
        {
            "role": "system",
            "content": RAW_PROMPT.format(
                prompt=prompt,
                clothing_items=clothing_items,
                output_attributes_description=OUTPUT_ATTRIBUTES_DESCRIPTION,
            ),
        }
    ]
    completion = LLMOpenAI().chat(model=model, messages=messages)
    output = completion.choices[0].message.content

    return output
