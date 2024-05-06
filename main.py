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

@tasks.loop(hours=24)
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
            await message.author.send('Thank you for your response! Enjoy your day.')
            print(f'DM received from {message.author.name}: {message.content}')

            user_file = os.path.join('responses', f"{message.author.display_name}.txt")
            if not os.path.exists(user_file):
                open(user_file, 'w').close()

            day_of_week = time.strftime('%A', time.localtime())

            response = f"{day_of_week}: {message.content}\n"
            with open(user_file, 'a', encoding='utf-8') as f:
                f.write(response)

def main():
    client.run(TOKEN)

if __name__ == '__main__':
    main()