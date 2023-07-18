import discord
from discord.ext import commands
import openai
from dotenv import load_dotenv
import os

# Load environmental variables from .env file
load_dotenv()

# Set up the OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define the Discord bot
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Implement the on_ready event
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Implement the on_message event
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore the bot's own messages

    # Extract the user's message
    user_message = message.content.replace(bot.user.mention, '')
    print(f"{message.author.name} said:\n{user_message}\n\n")

    # Generate a response using Chat-GPT
    response = generate_chat_response(user_message)
    print(f"GPT said:\n\n{response}\n\n")

    # Send the response back to the server
    await message.channel.send(f"{message.author.name} ---- My reply to you is:\n{response}")

    await bot.process_commands(message)

# Define the Chat-GPT model
def generate_chat_response(user_message):
    response = openai.Completion.create(
        engine='text-davinci-002',
        prompt=user_message,
        temperature=0.7,
        max_tokens=500,
        n=1,
        stop=None,
    )

    return response.choices[0].text.strip()

# Run the bot
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
