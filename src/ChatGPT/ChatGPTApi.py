import openai
import tiktoken as tiktoken


class ChatGPTBot:
    """
    ChatGPT API
    """

    ENCODER = tiktoken.encoding_for_model("gpt-3.5-turbo")

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

    def ask(self, message: str):
        """
            询问
        """
        self.__add_conversation("user", message)
        self.__truncate_conversation()
        try:
            resp = openai.ChatCompletion.create(
                model=self.model,
                messages=self.conversation
            )
            response_message = resp.choices[0].message.content
            response_role = resp.choices[0].message.role
        except openai.OpenAIError as e:
            response_message = str(e)
            response_role = "system"
        self.__add_conversation(response_role, response_message)
        return response_message

    def __add_conversation(self, role: str, content: str):
        """
        添加会话
        """
        self.conversation.append({"role": role, "content": content})
