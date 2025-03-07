import asyncio

async def chat(ctx):
    # conversation with chatbot from gpt.py at https://github.com/3r1cZ/Chatbot
    await ctx.send("Hi! I am Handler One, a bot with a slightly broken chat feature right now! Type anything to see what I'll say!")
    try:
        response = await ctx.bot.wait_for("message", timeout=20)

        output = ctx.bot.model.output(response.content)
        await ctx.send(output)
    except asyncio.TimeoutError: # when not answered after 20 seconds
        await ctx.send('You failed to answer in time!')

def setup(bot):
    bot.command()(chat)