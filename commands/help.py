async def help(ctx):
    help_file = open('help.txt', 'r')
    await ctx.send(help_file.read())
    help_file.close()

def setup(bot):
    bot.command()(help)