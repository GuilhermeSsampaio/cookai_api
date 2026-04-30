import json

from services.ai.personas import cookai_client, make_web_search_prompt
from settings.settings import GENAI_MODEL


def search_recipes_from_web(query: str):
    prompt_content = make_web_search_prompt(query)

    response = cookai_client.models.generate_content(
        model=GENAI_MODEL, contents=prompt_content
    )

    try:
        raw_text = response.text.strip()
        start_index = raw_text.find("[")
        end_index = raw_text.rfind("]")

        if start_index != -1 and end_index != -1:
            json_str = raw_text[start_index : end_index + 1]
            return json.loads(json_str)

        return {"error": "Model response was not a JSON list"}

    except Exception as exc:
        return {"error": f"Unable to parse response: {exc}"}
