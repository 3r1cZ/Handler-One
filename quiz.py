# This class implements the quiz feature of the discord bot

import asyncio
from random import randrange

def quiz(message, client):
  nextQuestion = True
  while nextQuestion:
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
          await message.channel.send('Exiting quiz.')
          return
        elif response.content.lower() == '*pass':
          await message.channel.send('Question passed. Next Question:')
          notCorrect = False
          nextQuestion = True
        elif response.content.lower() == answerList[randomQuestionNum]:
          await message.channel.send('Correct!')
          notCorrect = False
      except asyncio.TimeoutError:
        await message.channel.send('You failed to answer in time!')
        notCorrect = False

    questions.close()
    answers.close()