from pydantic import BaseModel, Field, validator
import re

class NewsInput(BaseModel):
    text: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="The news article text to analyze. Must be meaningful and between 10–5000 characters."
    )

    @validator("text")
    def validate_text(cls, value):
        # Reject text with only numbers or special characters
        if not re.search(r"[A-Za-z]", value):
            raise ValueError("Text must contain at least one alphabetic character.")
        # Reject if text is mostly whitespace
        if value.strip() == "":
            raise ValueError("Text cannot be empty or only spaces.")
        return value
