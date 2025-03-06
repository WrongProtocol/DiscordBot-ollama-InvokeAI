# Carmine Silano
# Feb 4, 2025
# A basic discord bot for providing access to ollama for gpt text and InvokeAI for image gen. 
# and features for checking our work calendar. 

import discord
import requests
import os
import asyncio
import tempfile
from discord.ext import commands
from dotenv import load_dotenv
from ollama_query import query_ollama
from invokeAI import create_hq
from helpers import *
from paymo_calendar import get_projects
from rvc import *

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


@bot.tree.command(name="gpt", description="Ask dolphin3 a question")
@discord.app_commands.describe(prompt="Ask dolphin3 a question")
async def gpt_slash(interaction: discord.Interaction, prompt: str):
    print(f"Slash command /gpt: {prompt}")
    await interaction.response.defer()
    
    # Run the query in a thread (or adjust as needed if query_ollama is async)
    response_text = await asyncio.to_thread(query_ollama, prompt, 'gpt')
    
    # If the response is short enough, send it directly.
    if len(response_text) <= 1990:
        await interaction.followup.send(response_text)
    else:
        # Otherwise, chunk the response and send each with a small delay.
        chunks = chunk_message(response_text, limit=1990)
        for chunk in chunks:
            await interaction.followup.send(chunk)
            await asyncio.sleep(1)  # delay between chunks


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

    if message.guild:

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
    else:
        # message is a direct message
        print("received a direct message")
        
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

@bot.tree.command(name="cal", description="Check the calendar for work")
@discord.app_commands.describe(prompt="search term. leave blank to see all.")
async def image_slash(interaction: discord.Interaction, prompt: str):
    print(f"Slash command /cal: {prompt}")
    await interaction.response.defer()
    
    filter = prompt.strip()
    
    if filter == "" or filter.lower() == "all":
        # show all
        resp = get_projects()
    else:
        # its a search name, so filter on that
        resp = get_projects(filter)
    
    resp = "Results for " + prompt + "\n" + resp
    await interaction.followup.send(resp)

@bot.tree.command(name="speak", description="Convert text to speech and send the audio file")
@discord.app_commands.describe(prompt="Enter text to convert to speech")
async def speak_slash(interaction: discord.Interaction, prompt: str):
    print(f"Slash command /speak: {prompt}")
    # Defer the response since TTS generation might take some time.
    await interaction.response.defer()
    
    # Await the asynchronous rvc_tts function directly.
    audio_file_path = await rvc_tts(prompt)
    
    # Create a Discord File object from the returned audio file path.
    audio_file = discord.File(audio_file_path, filename="fast_tts_output.mp3")
    
    # Send the audio file as a follow-up message.
    await interaction.followup.send(file=audio_file)

@bot.tree.command(name="erika", description="Process an attached audio file using rvc_erika and return the output audio file")
@discord.app_commands.describe(
                    file="Attach an audio file to process",
                    pitch_adjust="Enter an integer value for pitch adjustment (default: 0)")
async def erika_slash(interaction: discord.Interaction, file: discord.Attachment, pitch_adjust:int = 0):
    print(f"Slash command /erika invoked with file: {file.filename}")
    
    # Defer the response while processing.
    await interaction.response.defer()
    
    # Download the attached file as bytes.
    file_bytes = await file.read()
    
    # Write the downloaded bytes to a temporary file.
    suffix = os.path.splitext(file.filename)[1]  # Keep the original file extension
    with tempfile.NamedTemporaryFile(delete=False, prefix="erikaVO-", suffix=suffix) as tmp:
        tmp.write(file_bytes)
        tmp_input_path = tmp.name

    # Call rvc_erika (async) with the temporary file.
    output_audio_path = await rvc_erika(tmp_input_path, pitch_adjust)
    
    # remove the temporary input file.
    os.remove(tmp_input_path)
    
    # Create a Discord File object from the output audio file.
    audio_file = discord.File(output_audio_path, filename=os.path.basename(output_audio_path))
    
    # Send the output audio file back to the Discord channel.
    await interaction.followup.send(file=audio_file)

@bot.tree.command(name="cyrone", description="Process an attached audio file using rvc_cyrone and return the output audio file")
@discord.app_commands.describe(
                    file="Attach an audio file to process",
                    pitch_adjust="Enter an integer value for pitch adjustment (default: 0)")
async def cyrone_slash(interaction: discord.Interaction, file: discord.Attachment, pitch_adjust:int = 0):
    print(f"Slash command /cyrone invoked with file: {file.filename}")
    
    # Defer the response while processing.
    await interaction.response.defer()
    
    # Download the attached file as bytes.
    file_bytes = await file.read()
    
    # Write the downloaded bytes to a temporary file.
    suffix = os.path.splitext(file.filename)[1]  # Keep the original file extension
    with tempfile.NamedTemporaryFile(delete=False, prefix="cyroneVO-", suffix=suffix) as tmp:
        tmp.write(file_bytes)
        tmp_input_path = tmp.name

    # Call rvc_cyrone (async) with the temporary file.
    output_audio_path = await rvc_cyrone(tmp_input_path, pitch_adjust)
    
    # remove the temporary input file.
    os.remove(tmp_input_path)
    
    # Create a Discord File object from the output audio file.
    audio_file = discord.File(output_audio_path, filename=os.path.basename(output_audio_path))
    
    # Send the output audio file back to the Discord channel.
    await interaction.followup.send(file=audio_file)

# Finally, run the bot
bot.run(DISCORD_TOKEN)
