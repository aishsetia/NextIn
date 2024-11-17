import json
from base64 import b64encode
from fashion.clothes.models import LookType

from fashiongpt.core.llm import LLMOpenAI

output_format = """
```json
{
    "color": "color of the clothing item",
    "garment_type": "type of the clothing item",
    "patterns": "patterns on the clothing item",
    "look_type": "type of the look: should be one of [FORMAL, CASUAL, SPORTS, NIGHT_OUT, OTHER] strictly!"
}
```
"""

extract_attributes_raw_prompt = f"""
You are an expert in clothing and fashion. Your task is to analyse the given image and extract the attributes of the clothing items
The image of the clothing item is attached. The attributes should be in the following format:
{output_format}
DO NOT MISS ANY INFORMATION OR ADD ANY EXTRA INFORMATION THAT IS NOT IN THE IMAGE.
""".format(output_format=output_format)


def extract_attributes(image_fp: str) -> dict:
    llm = LLMOpenAI()

    message_with_image = {"role": "user", "content": []}
    message_with_image["content"].append(
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{b64encode(image_fp).decode('utf-8')}"},
        }
    )
    messages = [
        {"role": "system", "content": extract_attributes_raw_prompt},
        message_with_image,
    ]
    completion = llm.chat(model="gpt-4o", messages=messages)

    output = completion.choices[0].message.content

    return validate_and_parse_output(output)

def validate_and_parse_output(output: str) -> dict:
    try:
        output = json.loads(output)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON output")
    
    # check if all required fields are present
    if "color" not in output or "garment_type" not in output or "patterns" not in output or "look_type" not in output:
        raise ValueError("Missing required fields")
    
    # check if look_type is one of the allowed values
    if output["look_type"] not in [look_type.value for look_type in LookType]:
        raise ValueError("Invalid look_type")
    
    return output
