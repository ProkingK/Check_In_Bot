import os
import time
import discord

from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)

os.makedirs('responses', exist_ok=True)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    weekly_review.start()
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

@tasks.loop(hours=168)
async def weekly_review():
    channel = client.get_channel(int(CHANNEL_ID))
    for filename in os.listdir('responses'):
        file_path = os.path.join('responses', filename)
        if os.path.isfile(file_path):
            user_name = os.path.splitext(filename)[0]
            weekly_summary = f"Weekly review for {user_name}:\n"
            with open(file_path, 'r', encoding='utf-8') as f:
                contents = f.read()
                weekly_summary += contents + "\n"

            await channel.send(weekly_summary)

    for filename in os.listdir('responses'):
        file_path = os.path.join('responses', filename)
        os.remove(file_path)
    print('Weekly review sent and responses cleared.')

@client.event
async def on_message(message):
    if message.author != client.user:
        if isinstance(message.channel, discord.DMChannel):
            await message.author.send('Thank you for your response! Enjoy your day.')
            print(f'{message.author.name} sent: {message.content}')

            user_file = os.path.join('responses', f"{message.author.display_name}.txt")
            if not os.path.exists(user_file):
                open(user_file, 'w').close()

            day_of_week = time.strftime('%A', time.localtime())

            response = f"{day_of_week}: {message.content}\n"
            with open(user_file, 'a', encoding='utf-8') as f:
                f.write(response)

def main():
    client .run(TOKEN)

if __name__ == '__main__':
    main()