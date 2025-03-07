async def fun(ctx):
    await ctx.send("This is a fun command!")

def setup(bot):
    bot.command()(fun)