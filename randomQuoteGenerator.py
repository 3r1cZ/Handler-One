import pandas
from random import randrange
 
# reading the CSV file
csvFile = pandas.read_csv('AnimeQuotes.csv')
 
# displaying the contents of the CSV file
quotes = csvFile["Quote"].tolist()
characters = csvFile["Character"].tolist()
animes = csvFile["Anime"].tolist()

async def randomQuote(message):
    randomNum = randrange(len(quotes))
    toSend = '"' + quotes[randomNum] + '" - ' + characters[randomNum] + ', ' + animes[randomNum]
    await message.channel.send(toSend)