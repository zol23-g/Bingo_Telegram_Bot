from telethon import TelegramClient, events
import asyncio
from bingo_game import BingoGame
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = TelegramClient('bingo_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

game = BingoGame()

@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.respond("Welcome to BINGO! Type /join to join the game.")

@bot.on(events.NewMessage(pattern="/join"))
async def join(event):
    player_id = event.sender_id
    board = game.add_player(player_id)
    if board:
        board_str = "\n".join(["\t".join(map(str, row)) for row in board])
        await event.respond(f"Here is your BINGO board:\n\n{board_str}")
    else:
        await event.respond("You have already joined the game!")

@bot.on(events.NewMessage(pattern=r"/mark (\d+)"))
async def mark(event):
    number = int(event.pattern_match.group(1))
    player_id = event.sender_id
    if game.mark_number(player_id, number):
        if game.check_bingo(player_id):
            await event.respond("BINGO! You win! 🎉")
        else:
            await event.respond(f"Number {number} marked on your board!")
    else:
        await event.respond("Number not found on your board.")

async def main():
    print("Bot is running...")
    await bot.run_until_disconnected()

if __name__ == "__main__":
    bot.loop.run_until_complete(main())

