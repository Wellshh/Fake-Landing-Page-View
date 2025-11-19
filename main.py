import asyncio
from bot import TrafficBot

if __name__ == "__main__":
    try:
        bot = TrafficBot()
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        print("Bot stopped by user.")
    except Exception as e:
        print(f"Fatal error: {e}")
        exit(1)
