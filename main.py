import os
import discord
import re
from random import randrange
from keep_alive import keep_alive
from discord.ext import tasks
from itertools import cycle
from quiz import quiz

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

commandInProgress = False


@client.event
async def on_ready():
  change_status.start()
  print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  # returns when the author of a message is the bot itself
  if message.author == client.user:
    return

  # sends a text file containing all functions for the user to use
  if message.content == '*help':
    await message.channel.send(file=discord.File('help.txt'))

  global commandInProgress
  # generates a quiz for a user to guess when prompted by *quiz
  if message.content == '*quiz':
    if commandInProgress == False:
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

  # generates a random response to given keywords when prompted with *question
  keywordsYN = [
    'do', 'is', 'have', 'has', 'am', 'are', 'will', 'if', 'were', 'was',
    'should', 'would', 'does'
  ]
  patternYN = re.compile('|'.join(r'\b{}\b'.format(word)
                                  for word in keywordsYN))
  keywordsPercent = ['how', '%', 'percent', 'chance', 'probability']
  patternPercent = re.compile('|'.join(r'\b{}\b'.format(word)
                                       for word in keywordsPercent))
  if message.content.startswith('*question'):
    if 'how many' in message.content:
      num = randrange(10001)
      await message.channel.send(num)
    elif patternPercent.search(message.content) != None:
      num = randrange(101)
      await message.channel.send(str(num) + '%')
    elif patternYN.search(message.content) != None:
      answers = [
        'Yes', 'No', 'Maybe', 'Definitely', 'Definitely not', 'Not sure',
        'Up to you', 'Yeah', 'Nah', 'Yes LOL', 'No LOL'
      ]
      await message.channel.send(answers[randrange(len(answers))])
    else:
      emojis = open("emojis.txt", "r")
      EmojiList = emojis.readlines()
      await message.channel.send(EmojiList[randrange(len(EmojiList))])

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


status = cycle(['*help', '*quiz', '*question'])


@tasks.loop(seconds=180)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))


keep_alive()
client.run(os.getenv('token'))
