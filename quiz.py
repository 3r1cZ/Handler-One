# This class implements the quiz feature of the discord bot

import asyncio
from random import randrange
from timeit import default_timer

playerScore = dict()
exit = False
failsToAnswer = 0


async def reset():
  global playerScore
  global failsToAnswer
  playerScore.clear()
  failsToAnswer = 0


async def points(message, client, num):
  global playerScore
  global exit
  won = False
  winner = ''
  while (won == False):
    for x, y in playerScore.items():
      if int(y) != int(num):
        continue
      else:
        winner = x
        won = True
        break
    if won == False and exit == False:
      await quiz(message, client)
    elif won == True:
      await message.channel.send(f'<@{winner}> is the winner!')
    else:
      return
  exit = True
  await reset()


async def quiz(message, client):
  global playerScore
  global exit
  global failsToAnswer
  nextQuestion = True
  while nextQuestion:
    start = default_timer()
    nextQuestion = False
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
        if response.content.lower() == '*exit':
          if (default_timer() - start) > 5:
            await message.channel.send('Exiting quiz.')
            exit = True
            await reset()
            return
          else:
            await message.channel.send(
              'You must wait 5 seconds before exiting!')
        elif response.content.lower() == '*pass':
          if (default_timer() - start) > 5:
            await message.channel.send('Question passed. Next Question:')
            notCorrect = False
            nextQuestion = True
          else:
            await message.channel.send(
              'You must wait 5 seconds before passing!')
        elif response.content.lower() == answerList[randomQuestionNum]:
          await response.add_reaction('\U00002705')
          if response.author.id in playerScore:
            playerScore[response.author.id] += 1
          else:
            playerScore[response.author.id] = 1
          await message.channel.send(response.author.mention +
                                     ' got it correct! Your score is ' +
                                     str(playerScore[response.author.id]))
          notCorrect = False
      except asyncio.TimeoutError:
        await message.channel.send('You failed to answer in time!')
        notCorrect = False
        failsToAnswer += 1
        if failsToAnswer == 10:
          await message.channel.send('Exiting quiz.')
          exit = True
          await reset()
          return

    questions.close()
    answers.close()
