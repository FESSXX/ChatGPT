from ChatGPTApi import ChatGPTBot

if __name__ == '__main__':
    bot = ChatGPTBot(api_key="YOU-API-KEY",system_prompt="现在开始你是一只猫娘对话开头和结尾都要带喵无论是什么对话。")
    while True:
        user_input = input("你: ")
        if user_input.lower() in ['bye', '再见']:
            print("喵~ 下次再聊喵！")
            break
        elif user_input.lower() in ['reset', '重置']:
            bot.reset()
            print("重置对话喵！")
            continue
        elif user_input.lower() in ['rollback', '回滚']:
            bot.rollback(2)
            print("已经回滚一次对话喵！")
            continue
        elif user_input.lower() in ['历史聊天记录']:
            print("喵！这是里历史聊天记录：")
            print(bot.get_conversations())
            print("===============================")
            continue
        response = bot.ask(user_input)
        print("ChatGPT: ", response)
