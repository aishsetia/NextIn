from core.schemas import APIModel


class SuggestionResponse(APIModel):
    suggestion: str


class SuggestionRequest(APIModel):
    prompt: str
