from dataclasses import dataclass, field
from os import environ
from typing import List

from openai import OpenAI
from openai.types.chat import ChatCompletion

from app.gpt.constants import Model
from app.gpt.message import Message

@dataclass
class ChatGPTClient:
    model: Model
    messages: List[Message] = field(default_factory=list)
    client: OpenAI = field(init=False)

    def __post_init__(self) -> None:
        if not (key := environ.get("CHATGPT_API_KEY")):
            raise Exception("ChatGPT api key is not set as an environment variable")
        self.client = OpenAI(api_key=key)

    def add_message(self, message: Message) -> None:
        self.messages.append(message)

    def create(self) -> ChatCompletion:
        res = self.client.chat.completions.create(
            model=self.model.value,
            messages=[m.to_dict() for m in self.messages],
        )
        self.add_message(Message.from_dict(res.choices[0].message.dict()))
        return res