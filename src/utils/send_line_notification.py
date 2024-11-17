import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from linebot import LineBotApi
from linebot.models import TextSendMessage
from config.settings import LINE_CHANNEL_ACCESS_TOKEN, USER_ID


def send_line_notification(message):
    line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
    try:
        line_bot_api.push_message(USER_ID, TextSendMessage(text=message))
    except Exception as e:
        print(f"Failed to send message to LINE: {str(e)}")


# テスト用コード
if __name__ == "__main__":
    test_message = "This is a test message"
    send_line_notification(test_message)
