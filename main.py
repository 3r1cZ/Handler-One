import os
import discord
import asyncio
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
  # returns when the author of a message is the bot itself
  if message.author == client.user:
    return

  # generates a quiz for a user to guess when prompted with *quiz
  if message.content.startswith('*quiz'):
    questions = open("quizQuestions.txt", "r")
    questionList = questions.readlines()
    with open("quizAnswers.txt") as answers:
      answerList = answers.read().splitlines()
    randomQuestionNum = randrange(len(questionList))
    await message.channel.send(questionList[randomQuestionNum])

    # checking conditions for a response
    def check(response):
      return response.channel == message.channel

    # receiving user input
    notCorrect = True
    while (notCorrect):
      try:
        response = await client.wait_for("message", check=check, timeout=20)
        if response.content.lower() == answerList[randomQuestionNum]:
          await message.channel.send('Correct!')
          notCorrect = False
      except asyncio.TimeoutError:
        await message.channel.send('You failed to answer in time!')
        notCorrect = False

    questions.close()
    answers.close()

  # generates a random sentence from animes.txt when prompted by *recommend
  if message.content.startswith('*recommend'):
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
