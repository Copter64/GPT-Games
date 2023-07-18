import openai
import discord
import os
from discord.ext import commands

# Replace YOUR_DISCORD_BOT_TOKEN_ENV_VAR_NAME with the name of your Discord bot token environment variable
bot_token = os.getenv('DISCORD_BOT_TOKEN')

# Define the Discord bot
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, description="OpenAI bot")



# Replace YOUR_OPENAI_API_KEY_ENV_VAR_NAME with the name of your OpenAI API key environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define a dictionary to store conversation states for each user
conversation_states = {}

# Define a function to generate a response from OpenAI's API
def generate_response(input_text):
    prompt = f"User: {input_text}\nAI:"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

# Define a function to handle messages in a thread
async def handle_thread_message(message):
    if message.author.bot:
        return

    thread_id = message.reference.resolved.id
    user_id = message.author.id

    # Check if this is a new conversation thread for this user
    if user_id not in conversation_states or conversation_states[user_id]["thread_id"] != thread_id:
        conversation_states[user_id] = {"thread_id": thread_id, "conversation": []}

    # Add the user's message to the conversation history
    conversation_states[user_id]["conversation"].append(message.content)

    # Generate a response from OpenAI
    response_text = generate_response("\n".join(conversation_states[user_id]["conversation"]))

    # Send the response back in the thread
    await message.channel.send(response_text, reference=message)

# Define a command to test the bot
@bot.command()
async def test(ctx):
    await ctx.send("Hello, world!")

# Define a handler for thread messages
@bot.event
async def on_message(message):
    await handle_thread_message(message)


# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return  # Ignore the bot's own messages

#     # Ignore messages in regular channels
#     if not isinstance(message.channel, discord.Thread):
#         return



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Run the bot
bot.run(bot_token)
