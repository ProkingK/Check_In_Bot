import os
import time
import discord

from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    send_daily_message.start()

@tasks.loop(minutes=1)
async def send_daily_message():
    guild = client.guilds[0]
    members = [member for member in guild.members if not member.bot]
    for member in members:
        try:
            await member.send('Hey! What are you up to today?')
        except discord.HTTPException:
            print(f'Failed to send a message to {member}')

@client.event
async def on_message(message):
    if message.author != client.user:
        if isinstance(message.channel, discord.DMChannel):
            print(f'DM received from {message.author.name}: {message.content}')

def main():
    client.run(TOKEN)

if __name__ == '__main__':
    main()
