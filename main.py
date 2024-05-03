import os

from dotenv import load_dotenv
from discord import Intents, Client, Message

load_dotenv()

intents = Intents.default()
intents.message_content = True

client = Client(intents=intents)

async def send_message(message, user_message):
    response = f'Hello {message.author}, you said: "{user_message}"'
    await message.channel.send(response)

@client.event
async def on_ready():
    print(f'{client.user} is running')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    username = str(message.author)
    user_message = message.content
    channel = str(message.channel)

    print(f'{username} said: {user_message} in {channel}')

    await send_message(message, user_message)

def main():
    client.run(token=os.getenv('DISCORD_TOKEN'))

if __name__ == '__main__':
    main()