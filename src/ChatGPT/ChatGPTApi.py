import openai
import tiktoken as tiktoken


class ChatGPTBot:
    """
    ChatGPT API
    """

    def __init__(self, api_key: str, system_prompt: str = "you are ChatGPT"):
        self.model = "gpt-3.5-turbo"
        openai.api_key = api_key
        """
            初始模板对话 自定义
        """
        self.system_prompt = system_prompt
        self.conversation: list = [
            {
                "role": "system",
                "content": self.system_prompt,
            },
        ]
        self.max_tokens = 3000
        self.engine: str = "gpt-3.5-turbo"

    def ask(self, message: str) -> str:
        """
            询问
        """
        self.__add_conversation("user", message)
        self.__truncate_conversation()
        try:
            resp = openai.ChatCompletion.create(
                model=self.model,
                messages=self.conversation,
                max_tokens=self.get_max_token()
            )
            response_message = resp.choices[0].message.content
            response_role = resp.choices[0].message.role
        except openai.OpenAIError as e:
            response_message = str(e)
            response_role = "system"
        self.__add_conversation(response_role, response_message)
        return response_message

    def reset(self) -> None:
        """
        重置对话
        """
        self.conversation = [
            {"role": "system", "content": self.system_prompt},
        ]

    def rollback(self, n: int = 1) -> None:
        """
        回滚对话
        回滚默认回滚一条 但不是一次对话 即 USER：xxxx bot :xxx 回滚后 user：xxx
        若想回滚一次对话 请传入2
        """
        for _ in range(n):
            self.conversation.pop()

    def __add_conversation(self, role: str, content: str) -> None:
        """
        添加会话
        """
        self.conversation.append({"role": role, "content": content})

    def __truncate_conversation(self) -> None:
        """
        对话超长时截断对话
        """
        while True:
            if (
                    self.get_token_count() > self.max_tokens
                    and len(self.conversation) > 1
            ):
                self.conversation.pop(1)
            else:
                break

    def get_token_count(self) -> int:
        """
        获取token总数
        """
        encoding = tiktoken.encoding_for_model(self.engine)
        num_tokens = 0
        for message in self.conversation:
            num_tokens += 4
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += -1
        num_tokens += 2
        return num_tokens

    def get_max_token(self) -> int:
        """
        获取maxToken
        """

        return self.max_tokens - self.get_token_count()
