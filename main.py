import importlib
import os
import discord
from discord.ext import commands, tasks
from discord import app_commands
from itertools import cycle
from dotenv import load_dotenv
from keep_alive import keep_alive  # Assuming this keeps the bot alive in a hosting environment
import gpt as g  # Assuming this is your AI model

# Load environment variables
load_dotenv()
TOKEN = os.getenv('token')

# Define bot settings
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="*", intents=intents, help_command=None)
command_folder = "commands"  # Folder containing command files
model = g.model
status = cycle(['*help', '*quiz', '*bravery', '*play', '*chat'])

# Function to dynamically load commands
async def load_commands():
    command_files = [f for f in os.listdir("commands") if f.endswith(".py")]
    for file in command_files:
        module_name = f"commands.{file[:-3]}"
        spec = importlib.util.spec_from_file_location(module_name, f"commands/{file}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, "setup"):
            module.setup(bot)

@bot.event
async def on_ready():
    await load_commands()  # Load commands
    change_status.start()
    print(f'Logged in as {bot.user}')

# Task loop to change status
@tasks.loop(seconds=180)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

# Start bot
keep_alive()
bot.run(TOKEN)