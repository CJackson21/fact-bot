import discord
import json
import os
import random as r
import requests
from discord.ext import tasks
from dotenv import load_dotenv



CHANNEL_ID = 1054646631066255432
intents = discord.Intents.default()
bot = discord.Client(intents=intents)
load_dotenv()
API_KEY= os.getenv('API_KEY')


# Setting up intents for bot to receive events related to 
# server members and access content of messages.
intents = discord.Intents.default()
intents.members = True
intents.message_content = True



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

async def get_message():
    limit = 1
    api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
    response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
    if response.status_code == requests.codes.ok:
        data = json.loads(response.text)
        for item in data:
            print(f"Fact: {item['fact']}")
    else:
        print("Error:", response.status_code, response.text)

    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(response.text)

@tasks.loop(minutes=20.0)
async def send_fact():
    if r.randint(0, 100) < 5:
        get_message()




def run_bot(token):
    bot.run(token)


