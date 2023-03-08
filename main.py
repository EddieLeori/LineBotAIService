from lib.utility import *
from line_bot_ai_service import LineBotAIService

if __name__ == "__main__":
    linebot = LineBotAIService()
    linebot.run()
    Log("LineBotAIService close.")
    