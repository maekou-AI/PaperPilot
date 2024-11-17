from config.settings import LINE_CHANNEL_ACCESS_TOKEN, USER_ID


def main():
    print("Docker container is running")
    print(f"LINE_CHANNEL_ACCESS_TOKEN: {LINE_CHANNEL_ACCESS_TOKEN}")
    print(f"USER_ID: {USER_ID}")


if __name__ == "__main__":
    main()
