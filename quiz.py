# This class implements the quiz feature of the discord bot

import discord
import asyncio
from random import randrange
from timeit import default_timer

playerScore = dict()  # dictionary containing player scores
exit = False
failsToAnswer = 0

# reset states of variables when a game is finished
async def reset():
  global playerScore
  global failsToAnswer
  playerScore.clear()
  failsToAnswer = 0

# determines the current points of each user in order to determine how long to run the quiz for
async def points(message, client, num):
  global playerScore
  global exit
  won = False
  winner = ''
  while (won == False):
    for x, y in playerScore.items(): # checks if anyone has won
      if int(y) != int(num):
        continue
      else:
        winner = x
        won = True
        break
    if won == False and exit == False: # sends a quiz if nobody has won or the quiz has not been exited
      await quiz(message, client)
    elif won == True: # if someone has won
      await message.channel.send(f'<@{winner}> is the winner!')
    else:
      return
  exit = True
  await reset()

# outputting quizzes for the user
async def quiz(message, client):
  global playerScore
  global exit
  global failsToAnswer
  nextQuestion = True
  while nextQuestion: # posts a new question
    start = default_timer()
    nextQuestion = False
    # if music: # if music quiz has been requested
    #   with open("musicFiles/musicQuizQuestions.txt") as questions:
    #     questionList = questions.read().splitlines()
    #   with open("musicFiles/musicQuizAnswers.txt") as answers:
    #     answerList = answers.read().splitlines()
    #   randomQuestionNum = randrange(len(questionList))
    #   q = questionList[randomQuestionNum]
    #   await message.channel.send(file=discord.File(q))
    # else: # if a regular quiz has been requested
    questions = open("quizQuestions.txt", encoding="utf8")
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
    while notCorrect: # while an answer is incorrect, continue waiting for responses
      try:
        response = await client.wait_for("message", check=check, timeout=20)
        if response.content.lower() == '*exit':
          if (default_timer() - start) > 5: # exits quiz
            await message.channel.send('Exiting quiz.')
            exit = True
            await reset()
            return
          else: # if a user tries exiting a quiz within 5 seconds of a question being posted (prevents abuse of command)
            await message.channel.send(
              'You must wait 5 seconds before exiting!')
        elif response.content.lower() == '*pass':
          if (default_timer() - start) > 5: # passes question to new question
            await message.channel.send('Question passed. Next Question:')
            notCorrect = False
            nextQuestion = True
          else: # if a user tries passing within 5 seconds of a question being posted (prevents abuse of command)
            await message.channel.send(
              'You must wait 5 seconds before passing!')
        elif response.content.lower() == answerList[randomQuestionNum]: # if a response is correct
          await response.add_reaction('\U00002705')
          if response.author.id in playerScore: # checks if the user has been added to the dictionary of scores
            playerScore[response.author.id] += 1
          else:
            playerScore[response.author.id] = 1
          await message.channel.send(response.author.mention +
                                     ' got it correct! Your score is ' +
                                     str(playerScore[response.author.id]))
          notCorrect = False
      except asyncio.TimeoutError: # no response is received within 20 seconds
        await message.channel.send('You failed to answer in time!')
        notCorrect = False
        failsToAnswer += 1
        if failsToAnswer == 10: # if 10 questions receive no response in a row (prevents infinite questions from being asked)
          await message.channel.send('Exiting quiz.')
          exit = True
          await reset()
          return

  questions.close()
  answers.close()