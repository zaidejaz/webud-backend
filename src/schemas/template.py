from pydantic import BaseModel

class TemplatePrompt(BaseModel):
    prompt: str
