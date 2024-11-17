import json
import re

from .core.llm import LLMOpenAI, LLMOpenAIModels

raw_prompt = """
You are an expert consultant specializing in fashion. Your task is to analyse the given prompt and the descriptions of clothing items available with the user, and suggest a combination of clothing items to create a complete outfit.
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

output_attributes_description = """
1. **Comprehension:** Carefully read and understand the entire prompt above.
2. **Identification:** Identify all sections and requirements that are crucial for ideating the outfit.
3. **Extraction:** From these sections, extract attributes of clothing items that are relevant to the prompt.
4. **Matching:** Match the extracted attributes with the clothing items available with the user.
5. **Completion:** Find the best combination of clothing items that are relevant to the prompt, that would yield a complete outfit. This should include all items one would need to wear from top to bottom.
"""


def process_request_for_proposals(request_for_proposals: str) -> list[str]:
    model = LLMOpenAIModels.GPT_4O_MINI.value
    messages = [
        {
            "role": "system",
            "content": raw_prompt.format(
                request_for_proposals=request_for_proposals,
                output_attributes_description=output_attributes_description,
            ),
        }
    ]
    completion = LLMOpenAI(temperature=0.2).chat(model=model, messages=messages)
    output = completion.choices[0].message.content

    return output
