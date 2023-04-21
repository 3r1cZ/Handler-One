import os
import discord
from random import randrange
from keep_alive import keep_alive
from quiz import quiz

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

commandInProgress = False

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  # returns when the author of a message is the bot itself
  if message.author == client.user:
    return

  global commandInProgress
  # generates a quiz for a user to guess when prompted by *quiz
  if message.content == '*quiz':
    if(commandInProgress == False):
      commandInProgress = True
      await quiz(message, client)
      commandInProgress = False
    else:
      await message.channel.send('Quiz already in progress!')

  # generates a random sentence from animes.txt when prompted by *recommend
  if message.content == '*recommend':
    animes = open("animes.txt", "r")
    animeList = animes.readlines()
    await message.channel.send(animeList[randrange(len(animeList))])
    animes.close()

  # sends a goat emoji when a term/phrase in goats.txt is mentioned
  with open("goats.txt") as goats:
    goatList = goats.read().splitlines()
  words = message.content.split()
  for x in goatList:
    for i in range(len(words)):
      currentLength = i
      word = words[i]
      while (len(x) != len(word)):
        if len(x) < len(word):
          break
        elif len(x) > len(word):
          if currentLength == len(words) - 1:
            break
          currentLength += 1
          word = word + ' ' + words[currentLength]
      if x == word.lower():
        await message.channel.send('\U0001F410')
        return
  goats.close()


keep_alive()
client.run(os.getenv('token'))
