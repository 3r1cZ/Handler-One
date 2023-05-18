import os
import discord
import re
from random import randrange
from keep_alive import keep_alive
from discord.ext import tasks
from itertools import cycle
import quiz
import bravery
import music
import asyncio
from dotenv import load_dotenv

load_dotenv()

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
  if message.author == client.user or message.author.id == 432610292342587392:
    return

  # sends a text file containing all functions for the user to use
  if message.content == '*help':
    help = open('help.txt', 'r')
    await message.channel.send(help.read())
    help.close()

  if message.content == '*play':
    await music.play(message)
  
  if message.content.startswith('*playYoutube'):
    song = message.content[5: len(message.content)]
    await music.playYoutube(client, message, song)

  if message.content == ('*skip'):
    if music.vc is not None and music.vc:
        music.vc.stop()
        await message.channel.send('Song skipped!')
    else:
      await message.channel.send('Skip failed!')

  if message.content == ('*pause'):
    await message.channel.send('Song paused!')
    music.pause(music.vc)
  
  if message.content == ('*resume'):
    await message.channel.send('Song resumed!')
    music.resume(music.vc)

  if message.content == '*leave':
    await music.leave(message)
  global commandInProgress

  # checking conditions for a response
  def check(response):
    return response.channel == message.channel

  # generates a quiz for a user to guess when prompted by *quiz
  if message.content.startswith('*quiz'):
    musics = False
    if 'music' in message.content:
      musics = True
    if commandInProgress == False:
      commandInProgress = True
      await message.channel.send(
        'How many points would you like to play to? \nNote: you can use \*exit to end the quiz and \*pass to pass a question'
      )
      try:
        response = await client.wait_for("message", check=check, timeout=20)
        if response.content.isdigit() and int(response.content) != 0:
          quiz.exit = False
          await quiz.points(message, client, response.content, musics)
        else:
          await message.channel.send('This is not a valid number!')
      except asyncio.TimeoutError:
        await message.channel.send('You failed to answer in time!')

      commandInProgress = False
    else:
      await message.channel.send('Command already in progress!')

  # generates a random sentence from animes.txt when prompted by *recommend
  if message.content == '*recommend':
    animes = open("animes.txt", "r")
    animeList = animes.readlines()
    await message.channel.send(animeList[randrange(len(animeList))])
    animes.close()

  # ultimate bravery on League of Legends, randomizing most parts
  if message.content.startswith('*bravery'):
    if commandInProgress == False:
      commandInProgress = True
      if 'jg' in message.content:
        await bravery.bravery(message, client, True)
      else:
        await bravery.bravery(message, client, False)
      commandInProgress = False
    else:
      await message.channel.send('Command already in progress!')

  if message.content == '*valAgent':
    agents = open("BraveryValorant/valAgents.txt", "r")
    agentList = agents.readlines()
    await message.channel.send(agentList[randrange(len(agentList))])
    agents.close()

  if message.content.startswith('*valGun'):
    guns = open("BraveryValorant/valGuns.txt", "r")
    gunList = guns.readlines()
    if '1' == message.content[len(message.content) - 1] or '13' in message.content:
      await message.channel.send(gunList[randrange(5)])
    else:
      await message.channel.send(gunList[randrange(len(gunList))])
    guns.close()

  # generates a random response to given keywords when prompted with *question
  keywordsNum = ['how many', 'number of', 'number']
  patternNum = re.compile('|'.join(r'\b{}'.format(word)
                                   for word in keywordsNum))
  keywordsYN = [
    'do', 'is', 'have', 'has', 'am', 'are', 'will', 'if', 'were', 'was',
    'should', 'would', 'does', '=', 'equals', 'equal', '=='
  ]
  keywordsYNSpecial = ['=', '==']
  patternYN = re.compile('|'.join(r'\b{}'.format(word) for word in keywordsYN))
  patternYNSpecial = re.compile('|'.join(word for word in keywordsYNSpecial))

  keywordsPercent = ['how much', 'percent', 'chance', 'probability']
  patternPercent = re.compile('|'.join(r'\b{}'.format(word)
                                       for word in keywordsPercent))
  if message.content.startswith('**'):
    if patternNum.search(message.content.lower()) != None:
      num = randrange(1001)
      await message.channel.send(num)
    elif patternPercent.search(message.content.lower()) != None or re.search(
        '%', message.content) != None:
      num = randrange(101)
      await message.channel.send(str(num) + '%')
    elif patternYN.search(
        message.content.lower()) != None or patternYNSpecial.search(
          message.content.lower()) != None:
      answers = [
        'Yes', 'No', 'Maybe', 'Definitely', 'Definitely not', 'Not sure',
        'Up to you', 'Yeah', 'Nah', 'Yes LOL', 'No LOL', 'Probably'
      ]
      await message.channel.send(answers[randrange(len(answers))])
    else:
      emojis = open("emojis.txt", "r")
      EmojiList = emojis.readlines()
      await message.channel.send(EmojiList[randrange(len(EmojiList))])
      emojis.close()

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


status = cycle(['*help', '*quiz', '*bravery', '*play'])


@tasks.loop(seconds=180)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))

keep_alive()
client.run(os.getenv('token'))
