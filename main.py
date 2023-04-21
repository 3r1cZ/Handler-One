import os
import discord
from random import randrange
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  goats = ['oshi', '86', 'love is war']
  if message.content.startswith('*recommend'):
    animes = [
      'If you are into shonen, watch Demon Slayer',
      '86 is one of the best political dramas',
      'Love is War is the greatest romance of all time',
      'If you love overpowered isekai, watch Overlord or Eminence in Shadow'
    ]
    await message.channel.send(animes[randrange(len(animes))])

  for x in goats:
    if x in message.content.lower():
      await message.channel.send('\U0001F410')


keep_alive()
client.run(os.getenv('token'))
