from lib.utility import *
from app import LineBotAIService

if __name__ == "__main__":
    linebot = LineBotAIService()
    linebot.run()
    Log("LineBotAIService close.")
    