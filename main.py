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
import randomQuoteGenerator
from dotenv import load_dotenv
import gpt as g

model = g.model # AI model

load_dotenv() # using environment variables

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# for song storage
song1 = ''
song2 = ''
# initalizing two lists of songs for multiple pages in a message
for i in range(50):
  song1+=('[' + str(i+1) + '] ' + music.answerList[i] + '\n')
for i in range(50,len(music.answerList[i])):
  song2+=('[' + str(i+1) + '] ' + music.answerList[i] + '\n')
contents = [song1, song2] # holds pages of songs

commandInProgress = False # if a command is currently in progress (for *quiz and *bravery only)

# dropdown menu for selection and sorting when running *playsong
class Select(discord.ui.Select):
    global song1
    global song2
    global contents
    def __init__(self):
        options=[
            discord.SelectOption(label="No Sort",description="Original listing (by date added)"),
            discord.SelectOption(label="Sort by Anime",description="Sort the list of songs by anime title"),
            discord.SelectOption(label="Sort by Song",description="Sort the list of songs by song title"),
            ]
        super().__init__(placeholder="Sorting Options",max_values=1,min_values=1,options=options)
    async def callback(self, interaction: discord.Interaction):
        global song1
        global song2
        global contents
        if self.values[0] == "No Sort": # default sorting (by date added)
          # reset all three lists
          with open("musicFiles/musicQuizAnswers.txt") as songs:
            music.answerList = songs.read().splitlines()
          with open("musicFiles/musicQuizQuestions.txt") as songs:
            music.questionList = songs.read().splitlines()
          music.animeList = []
          with open("musicFiles/musicQuizAnswers.txt") as answers: # list of anime titles only (recorded after a '-' in the input)
            for line in answers:
                for i in range(len(line)):
                    if line[i] == ' ' and line[i+1] == '-':
                          title = line[i+3:-1]
                          music.animeList.append(title)
          answers.close()
          songs.close()
          song1 = ''
          song2 = ''
          for i in range(50):
            song1+=('[' + str(i+1) + '] ' + music.answerList[i] + '\n')
          for i in range(50,len(music.answerList)):
            song2+=('[' + str(i+1) + '] ' + music.answerList[i] + '\n')
          contents = [song1, song2]
          await interaction.response.edit_message(content='```' + song1 + '```')

        elif self.values[0] == "Sort by Anime": # sorting by anime title
            music.quickSort(music.animeList, 0, len(music.animeList)-1)
            song1 = ''
            song2 = ''
            for i in range(50):
              song1+=('[' + str(i+1) + '] ' + music.answerList[i] + '\n')
            for i in range(50,len(music.answerList)):
              song2+=('[' + str(i+1) + '] ' + music.answerList[i] + '\n')
            contents = [song1, song2]
            await interaction.response.edit_message(content='```' + song1 + '```')

        elif self.values[0] == "Sort by Song": # sorting by song title
            music.quickSort(music.answerList, 0, len(music.answerList)-1)
            song1 = ''
            song2 = ''
            for i in range(50):
              song1+=('[' + str(i+1) + '] ' + music.answerList[i] + '\n')
            for i in range(50,len(music.answerList)):
              song2+=('[' + str(i+1) + '] ' + music.answerList[i] + '\n')
            contents = [song1, song2]
            await interaction.response.edit_message(content='```' + song1 + '```')

# viewing the select menu created in Select()
class SelectView(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
        self.add_item(Select())

@client.event
async def on_ready():
  change_status.start()
  print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  global commandInProgress

  # does not run a command when the author of a message is the bot itself
  if message.author == client.user or message.author.id == 432610292342587392:
    return

  # checking conditions for a response
  def check(response):
    return response.channel == message.channel and response.author == message.author
  
  # sends a text file containing all functions for the user to use
  if message.content.lower() == '*help':
    help = open('help.txt', 'r')
    await message.channel.send(help.read())
    help.close()

  # list of valid commands
  musicCommands = ['*play', '*playyoutube', '*playsong', '*loop', '*repeat', '*skip', '*pause', '*resume', '*leave']
  inCommands = False
  # checks if the message contains any of the above commands
  for command in musicCommands:
      if command in message.content:
        inCommands = True
        break
  if message.author.voice != None: # if in a voice channel
    if inCommands:
      
      # plays music from an mp3 file in a voice channel
      if message.content.lower() == '*play':
        await music.play(message, None)
      
      # plays music from a YouTube URL in a voice channel
      elif message.content.lower().startswith('*playyoutube'):
        song = message.content[5: len(message.content)]
        await music.playYoutube(client, message, song)
      
      # plays a specific song from a given list
      elif message.content.lower() == '*playsong':
        myMessage = await message.channel.send('```' + song1 + '```', view = SelectView()) # sends a list of songs
        await myMessage.add_reaction("\u25c0") # backwards
        await myMessage.add_reaction("\u25b6") # forwards
        await myMessage.add_reaction('\U00002705')
        await myMessage.channel.send('Please click on the checkmark when finished looking at the list:')
        
        cur_page = 1 # current page
        # checks if user reaction is valid
        def checkTwo(reaction, user):
            return user == message.author and str(reaction.emoji) in ["\u25c0", "\u25b6", '\U00002705']
        
        # reaction loop
        while True: 
          try:
              # waiting for a reaction to be added - times out after 60 seconds
              reaction, user = await client.wait_for("reaction_add", check=checkTwo, timeout=60)

              if str(reaction.emoji) == "\u25b6" and cur_page != len(contents): # next page reaction
                  cur_page += 1
                  await myMessage.edit(content='```' + contents[cur_page-1] + '```')
                  await myMessage.remove_reaction(reaction, user)
              elif str(reaction.emoji) == "\u25c0" and cur_page > 1: # back page reaction
                  cur_page -= 1
                  await myMessage.edit(content='```' + contents[cur_page-1] + '```')
                  await myMessage.remove_reaction(reaction, user)
              elif str(reaction.emoji) == '\U00002705': # reaction to end loop
                break
              else:
                  # removes reactions if the user tries to go forward on the last page or backwards on the first page
                  await myMessage.remove_reaction(reaction, user)
          except asyncio.TimeoutError: # timed out
            await message.channel.send('Time expired.')
            break
        
        await message.channel.send('Enter a number from a song in the above list:')

        # user response
        try:
          response = await client.wait_for("message", check=check, timeout=60)
          # if response is a number on the list of songs
          if response.content.isdigit() and int(response.content) >=1 and int(response.content) <=len(music.answerList):
            await music.playSong(message, int(response.content)-1)
          else:
            await message.channel.send('This is not a valid number!')
        except asyncio.TimeoutError: # timed out
          await message.channel.send('You failed to answer in time!')

      # playing a random song 
      elif message.content.lower().startswith('*play'):
        num = message.content[6: len(message.content)] # duration (if given)
        if num.isdigit() == False or int(num) >90: # must be a number and cannot be played for more than 90 seconds
          await message.channel.send('Invalid time.')
        else:
          await music.play(message, num)

      # looping a song
      if message.content.lower() == '*loop':
        if message.guild.voice_client: # If the bot is in a voice channel 
          if music.loops: # if already looped
            music.loops = False
            await message.add_reaction('\U00002705')
            await message.channel.send('Loop stopped!')
          else: # if not looped yet
            music.loops = True
            await message.add_reaction('\U00002705')
            await message.channel.send('Loop started!')
        else:
          await message.channel.send('Loop Failed!')
      
      # repeats a song
      if message.content.lower().startswith('*repeat'):
        num = message.content[8: len(message.content)] # duration of repeat (required)

        # if no numbers or greater than 90 seconds or index not initialized (no song) or time not initialized (when initially playing a song)
        if num.isdigit() == False or int(num) >90 or music.index == -1 or music.timeGlobal == -1:
          await message.channel.send('Repeat Failed!')
        else:
          music.timeGlobal = num
          await message.add_reaction('\U00002705')
          await music.repeat()
        
      # skips the current song playing and plays a new song
      if message.content.lower() == '*skip':
        if music.vc is not None and music.vc and message.guild.voice_client:
            music.vc.stop()
            await message.channel.send('Song skipped!')
        else:
          await message.channel.send('Skip failed!')

      # pauses the current song
      if message.content.lower() == ('*pause'):
        if music.vc is not None and music.vc and message.guild.voice_client:
          await message.channel.send('Song paused!')
          music.pause(music.vc)
        else:
          await message.channel.send('Pause failed!')
      
      # resumes the current song
      if message.content.lower() == ('*resume'):
        if music.vc is not None and music.vc and message.guild.voice_client:
          await message.channel.send('Song resumed!')
          music.resume(music.vc)
        else:
          await message.channel.send('Resume failed!')

      # makes the bot leave the voice channel it is currently in
      if message.content.lower() == '*leave':
        await music.leave(message)

  elif inCommands and message.author.voice == None: # not in voice channel but a command is used
    await message.channel.send('Must be in a voice channel to use this command!')

  # generates a quiz for a user to guess when prompted by *quiz
  if message.content.lower() == '*quiz':

    # musics = False
    # if 'music' in message.content: # checks if the user is asking for a music quiz instead of a normal one
    #   musics = True

    if commandInProgress == False:
      commandInProgress = True
      # waits for a response from the user regarding number of points
      await message.channel.send(
        'How many points would you like to play to? \nNote: you can use \*exit to end the quiz and \*pass to pass a question'
      )
      try:
        response = await client.wait_for("message", check=check, timeout=20)
        if response.content.isdigit() and int(response.content) > 0 and int(response.content) <= 100:
          quiz.exit = False
          await quiz.points(message, client, response.content) # run the quiz
        else:
          await message.channel.send('This is not a valid number!')
      except asyncio.TimeoutError: # when not answered after 20 seconds
        await message.channel.send('You failed to answer in time!')

      commandInProgress = False
    else:
      await message.channel.send('Command already in progress!')

  # conversation with chatbot from gpt.py at https://github.com/3r1cZ/Chatbot
  if message.content.lower() == '*chat':
    await message.channel.send("Hi! I am Handler One, a bot with a slightly broken chat feature right now! Type anything to see what I'll say!")
    try:
      response = await client.wait_for("message", timeout=20)

      output = model.output(response.content)
      await message.channel.send(output)
    except asyncio.TimeoutError: # when not answered after 20 seconds
      await message.channel.send('You failed to answer in time!')

  # generates a random quote from AnimeQuotes.csv
  if message.content.lower() == '*quote':
    toSend = randomQuoteGenerator.randomQuote()
    await message.channel.send(toSend)

  # ultimate bravery on League of Legends, randomizing builds for champions
  if message.content.lower().startswith('*bravery'):
    if commandInProgress == False:
      commandInProgress = True
      if 'jg' in message.content: # gives guaranteed smite for junglers
        await bravery.bravery(message, client, True)
      else:
        await bravery.bravery(message, client, False)
      commandInProgress = False
    else:
      await message.channel.send('Command already in progress!')

  # sends a random agent from Valorant to the text channel
  if message.content.lower() == '*valagent':
    agents = open("BraveryValorant/valAgents.txt", "r")
    agentList = agents.readlines()
    await message.channel.send(agentList[randrange(len(agentList))])
    agents.close()

  # sends a random gun from Valorant to the text channel
  if message.content.lower().startswith('*valgun'):
    guns = open("BraveryValorant/valGuns.txt", "r")
    gunList = guns.readlines()
    if '1' == message.content[len(message.content) - 1] or '13' in message.content:
      await message.channel.send(gunList[randrange(5)])
    else:
      await message.channel.send(gunList[randrange(len(gunList))])
    guns.close()

  # generates a random response to given keywords when prompted with **
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
    if patternNum.search(message.content.lower()) != None: # checking first set of keywords (keywordsNum)
      num = randrange(1001)
      await message.channel.send(num)
    elif patternPercent.search(message.content.lower()) != None or re.search(
        '%', message.content) != None: # checking second set of keywords (keywordsPercent)
      num = randrange(101)
      await message.channel.send(str(num) + '%')
    elif patternYN.search(
        message.content.lower()) != None or patternYNSpecial.search(
          message.content.lower()) != None: # checking third set of keywords (keywordsYN and keywordsYNSpecial)
      answers = [
        'Yes', 'No', 'Maybe', 'Definitely', 'Definitely not', 'Not sure',
        'Up to you', 'Yeah', 'Nah', 'Yes LOL', 'No LOL', 'Probably'
      ]
      await message.channel.send(answers[randrange(len(answers))])
    else: # if none of the keywords are hit
      emojis = open("emojis.txt", "r")
      EmojiList = emojis.readlines()
      await message.channel.send(EmojiList[randrange(len(EmojiList))])
      emojis.close()

  # sends a goat emoji when a term/phrase in goats.txt is mentioned
  with open("goats.txt") as goats:
    goatList = goats.read().splitlines()
  words = message.content.split()
  # checks if each phrase in goatList is an exact match of some words in a message
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

# discord status display
status = cycle(['*help', '*quiz', '*bravery', '*play', '*chat'])

@tasks.loop(seconds=180)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))

# run the bot
keep_alive()
client.run(os.getenv('token'))