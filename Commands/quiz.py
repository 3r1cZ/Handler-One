# This class implements the quiz feature of the discord bot
import asyncio
from random import randrange
from timeit import default_timer

playerScore = dict()  # dictionary containing player scores
exit = False
failsToAnswer = 0

async def predicate(ctx):
    try:
        num = int(ctx.message.content.split()[1])  # Get the first argument
        return 1 <= num <= 100  # Allow only numbers from 1 to 100
    except (ValueError, IndexError):
        return False  # Reject invalid values

# reset states of variables when a game is finished
async def reset():
  global playerScore
  global failsToAnswer
  playerScore.clear()
  failsToAnswer = 0

# determines the current points of each user in order to determine how long to run the quiz for
async def points(ctx, num: int):
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
      await quiz(ctx)
    elif won == True: # if someone has won
      await ctx.send(f'<@{winner}> is the winner!')
    else:
      return
  exit = True
  await reset()

# outputting quizzes for the user
async def quiz(ctx):
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
    #   await ctx.send(file=discord.File(q))
    # else: # if a regular quiz has been requested
    questions = open("quizQuestions.txt", encoding="utf8")
    questionList = questions.readlines()
    with open("quizAnswers.txt") as answers:
      answerList = answers.read().splitlines()
    randomQuestionNum = randrange(len(questionList))
    await ctx.send(questionList[randomQuestionNum])

    # checking conditions for a response
    def check(response):
      return response.channel == ctx.channel

    # receiving user input
    notCorrect = True
    while notCorrect: # while an answer is incorrect, continue waiting for responses
      try:
        response = await ctx.bot.wait_for("message", check=check, timeout=20)
        if response.content.lower() == '*exit':
          if (default_timer() - start) > 5: # exits quiz
            await ctx.send('Exiting quiz.')
            exit = True
            await reset()
            return
          else: # if a user tries exiting a quiz within 5 seconds of a question being posted (prevents abuse of command)
            await ctx.send(
              'You must wait 5 seconds before exiting!')
        elif response.content.lower() == '*pass':
          if (default_timer() - start) > 5: # passes question to new question
            await ctx.send('Question passed. Next Question:')
            notCorrect = False
            nextQuestion = True
          else: # if a user tries passing within 5 seconds of a question being posted (prevents abuse of command)
            await ctx.send(
              'You must wait 5 seconds before passing!')
        elif response.content.lower() == answerList[randomQuestionNum]: # if a response is correct
          await response.add_reaction('\U00002705')
          if response.author.id in playerScore: # checks if the user has been added to the dictionary of scores
            playerScore[response.author.id] += 1
          else:
            playerScore[response.author.id] = 1
          await ctx.send(response.author.mention +
                                     ' got it correct! Your score is ' +
                                     str(playerScore[response.author.id]))
          notCorrect = False
      except asyncio.TimeoutError: # no response is received within 20 seconds
        await ctx.send('You failed to answer in time!')
        notCorrect = False
        failsToAnswer += 1
        if failsToAnswer == 10: # if 10 questions receive no response in a row (prevents infinite questions from being asked)
          await ctx.send('Exiting quiz.')
          exit = True
          await reset()
          return
  questions.close()
  answers.close()

def setup(bot):
    bot.command(name="quiz")(points)