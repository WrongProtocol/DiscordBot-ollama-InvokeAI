# Carmine Silano
# Feb 4, 2025
# A basic discord bot for providing access to ollama for gpt text and InvokeAI for image gen. 

import discord
import requests
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from ollama_query import query_ollama
from invokeAI import create_hq

# Load secret environment variables
load_dotenv('.env')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_PERMISSIONS_INT = int(os.getenv('DISCORD_PERMISSIONS_INT', 0))

# Global flag to determine whether to respond to all messages in #test
respond_to_all = True

# Set up intents for the bot
intents = discord.Intents.default()
intents.message_content = True

# Set up the bot with a command prefix of '!'
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    # Notify when the bot has connected to Discord
    print(f'{bot.user.name} has connected to Discord!', flush=True)
    permissions = discord.Permissions(DISCORD_PERMISSIONS_INT)
    invite_url = discord.utils.oauth_url(bot.user.id, permissions=permissions)
    print("Invite URL:", invite_url)

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print("Error syncing commands:", e)

# Slash command for GPT queries
@bot.tree.command(name="gpt", description="Ask dolphin3 a question")
@discord.app_commands.describe(prompt="Ask dolphin3 a question")
async def gpt_slash(interaction: discord.Interaction, prompt: str):
    print(f"Slash command /gpt: {prompt}")
    await interaction.response.defer()
    response_text = await asyncio.to_thread(query_ollama, prompt, 'gpt')
    await interaction.followup.send(response_text)

# Slash command for writing voice overs or lyrics
@bot.tree.command(name="write", description="Write voice overs or lyrics about your topic.")
@discord.app_commands.describe(prompt="The topic you want to write about")
async def write_slash(interaction: discord.Interaction, prompt: str):
    print(f"Slash command /write: {prompt}")
    await interaction.response.defer()
    response_text = await asyncio.to_thread(query_ollama, prompt, 'vo')
    await interaction.followup.send(response_text)

# Slash command for converting rude talk into kind language
@bot.tree.command(name="kindly", description="Convert rude, nasty talk into kind and professional language")
@discord.app_commands.describe(prompt="The nasty phrase you want to make sound kind and profesh.")
async def kindly_slash(interaction: discord.Interaction, prompt: str):
    print(f"Slash command /kindly: {prompt}")
    await interaction.response.defer()
    response_text = await asyncio.to_thread(query_ollama, prompt, 'kindly')
    await interaction.followup.send(response_text)

# Event listener to respond to all messages in the #test channel if the flag is True.
@bot.event
async def on_message(message: discord.Message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Check if the message was sent in a channel named "test" and if the flag is enabled
    if message.channel.name == "test" and respond_to_all and bot.user not in message.mentions:
        
        print(f"Responding to message in #test: {message.content}")
        
        # Grab the last 50 messages from the channel's history
        messages = [msg async for msg in message.channel.history(limit=50)]
        # Reverse the list to have chronological order
        messages = list(reversed(messages))
        # Create a context string in the format "Author: message"
        context = "\n".join(f"{msg.author.display_name}: {msg.content}" for msg in messages)
        # Append the current message as the new prompt with context
        prompt_with_context = f"Chat history:\n{context}\n\nNew message: {message.content}\n\nResponse:"
        
        # Call query_ollama with the prompt that includes context (using 'gpt' mode)
        response_text = await asyncio.to_thread(query_ollama, prompt_with_context, 'continuous_chat')
        await message.channel.send(response_text)
    
    # If the bot is mentioned, respond to the mention.
    if bot.user in message.mentions:
        
        prompt = message.content.replace(f"<@!{bot.user.id}>", "").strip()
        response_text = await asyncio.to_thread(query_ollama, prompt, 'respond_to_mention')
        await message.channel.send(response_text)
        
        return
    
    # Allow commands to be processed as well
    await bot.process_commands(message)

@bot.tree.command(name="image", description="Generate a high quality image from a prompt in ~20 seconds")
@discord.app_commands.describe(prompt="Enter your image generation prompt. Allow 20sec for generation.")
async def image_slash(interaction: discord.Interaction, prompt: str):
    print(f"Slash command /image: {prompt}")
    await interaction.response.defer()
    
    # Directly await the asynchronous create_hq function.
    image_data = await create_hq(prompt)
    
    image_file = discord.File(image_data, filename="generated.png")
    await interaction.followup.send(content="Here is your image:", file=image_file)



# Run the bot
bot.run(DISCORD_TOKEN)
