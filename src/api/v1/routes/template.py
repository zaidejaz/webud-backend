import json
from pathlib import Path
from fastapi import APIRouter

from src.schemas.template import TemplatePrompt
from src.utils.llm import get_llm_response

router = APIRouter()

@router.post("/template")
async def template(prompt: TemplatePrompt):
    if not prompt.prompt:
        return {"error": "Prompt is required"}
    messgage = f"""Please return either nextjs, vite or node based on the prompt. Important! Return only one word
    Example: Create a todo app in nextjs Output: next
    Example: Create a todo app in vite Output: react
    Example: Create a todo app in node Output: node
    {prompt}
    """
    try:
        template = get_llm_response(messgage)
        print(template)
        with open(f"src/templates/{template}.json", "r") as f:
            template = json.load(f)
        return {"template": template}
    except Exception as e:
        return {"error": str(e)}
