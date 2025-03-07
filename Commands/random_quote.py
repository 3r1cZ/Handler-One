import pandas
from random import randrange
 
# reading the CSV file
csvFile = pandas.read_csv('AnimeQuotes.csv')
 
# displaying the contents of the CSV file
quotes = csvFile["Quote"].tolist()
characters = csvFile["Character"].tolist()
animes = csvFile["Anime"].tolist()

# returns a random quote from the above dataset
async def quote(ctx):
    randomNum = randrange(len(quotes))
    toSend = '"' + quotes[randomNum] + '" - ' + characters[randomNum] + ', ' + animes[randomNum]
    await ctx.send(toSend)

def setup(bot):
    bot.command()(quote)