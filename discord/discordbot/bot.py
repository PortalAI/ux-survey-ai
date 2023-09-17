import discord
from discord.ext import commands, tasks
import os
import json
from datetime import datetime, timedelta
import requests
import logging
from dotenv import load_dotenv
load_dotenv()

# LangChain
from agent import langchain_agent

logger = logging.getLogger('discord')

TIMEDELTA = 1  # Minutes

TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
BACKEND_DYNAMIC_PROMPT_ENDPOINT = "https://survey-bot.portal-ai-dev.com/guide_prompt/"
BACKEND_CHAT_STORE_ENDPOINT = "https://survey-bot.portal-ai-dev.com/save_discord_chat_result/"
CONTACTED_USERS_FILE = "contacted_users.json"

AGI_HOUSE_GUILD_ID = "1136052748262060113"
TEST_GUILD_ID = "1151951195091513396"

SUMMARIZATION_PROMPT = """
Please help summarize the chat above.
"""

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True
intents.dm_messages = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

users_to_agents = {}  # The in-memory dictionary of conversational agents for each user

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user.name}({bot.user.id})')
    check_for_expired_chats.start()

@bot.event
async def on_guild_join(guild):
    logger.info(f"Connected to {guild.name}({guild.id}). Total members: {guild.member_count}. Fetching prompt...")
    
    # Announce the bot in the guild through the general chat
    channel = guild.system_channel or next((channel for channel in guild.text_channels if channel.permissions_for(guild.me).send_messages), None)
    
    if not channel:
        logger.error(f"Could not send a message to the guild {guild.name}({guild.id}). No system channel or text channels with send_messages permission found!")
        return
    
    # TODO: Dynamic first message instead?
    await channel.send("Hello everyone! DM me to complete a special survey and get a reward! 🚀")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    author_id = str(message.author.id)

    # Message is a DM
    if message.guild is None:  
        logger.info(f"Received a DM from {message.author.name}({message.author.id}): {message.content}")

        agent = None
        response = None
        # it's the first time this user is contacting the bot, need to create a new agent
        if author_id not in users_to_agents:
            guild_origin = None
            for guild in bot.guilds:
                if guild.get_member(message.author.id):
                    guild_origin = guild
                    break
            
            agent = generate_agent_for_user()
            # TODO: remove hardcoded guild_id
            msg = fetch_prompt_for_guild(AGI_HOUSE_GUILD_ID, message.author.name) + "\n\n" + message.content
            # msg = fetch_prompt_for_guild(guild_origin.name, message.author.name) + "\n\n" + message.content
            response = agent.generate_response(msg)
            users_to_agents[author_id] = {
                'agent': agent,
                'timestamp': datetime.utcnow().isoformat()
            }
        else:
            agent = users_to_agents[author_id]['agent']
            response = agent.generate_response(message.content)
        
        # Update the timestamp for the user
        users_to_agents[author_id]['timestamp'] = datetime.utcnow().isoformat()
        
        # print(f"Complete chat:\n{agent.memory.buffer}")
        
        await message.channel.send(response)

    await bot.process_commands(message)


def fetch_prompt_for_guild(guild_name, user_name):
    response = requests.get(BACKEND_DYNAMIC_PROMPT_ENDPOINT + guild_name)
    if response.status_code == 200:
        # we receive back a string
        prompt = response.json()
        logger.info(f"Received prompt for guild {guild_name}: {prompt}")
        return prompt
    else:
        logger.error(f"Could not fetch prompt for guild {guild_name}. Status code: {response.status_code}")
        return None


def generate_agent_for_user():
    return langchain_agent.LangChainAgent()


@tasks.loop(minutes=TIMEDELTA)
async def check_for_expired_chats():
    logger.info("Checking for expired chats")
    current_time = datetime.utcnow()
    expired_chats = []

    for user_id, data in users_to_agents.items():
        last_message_time = datetime.fromisoformat(data['timestamp'])
        if current_time - last_message_time > timedelta(minutes=TIMEDELTA):
            expired_chats.append(user_id)
            logger.info(f"Expired chat with user {user_id}")

    # Dump these chats to the backend
    for user_id in expired_chats:
        agent = users_to_agents.pop(user_id)['agent']
        # get the chat
        complete_chat = agent.memory.buffer
        # get the user and guild ids
        guild_origin = None
        member_name = None
        for guild in bot.guilds:
            member = guild.get_member(user_id)
            if member:
                guild_origin = guild
                member_name = member.name
                break
        # TODO: remove fallback with better fetch logic
        guild_id = guild_origin.id if guild_origin else AGI_HOUSE_GUILD_ID
        
        summary = agent.generate_response(SUMMARIZATION_PROMPT)
        print(f"Dumping {guild_id} <> {user_id} <> {member_name} <> {summary}")
        
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        
        # Create the payload
        data = {
            "guild_id": guild_id,
            "user_id": user_id,
            "summary": summary,
            "chat_history": complete_chat
        }
        
        # Send the POST request
        response = requests.post(BACKEND_CHAT_STORE_ENDPOINT, headers=headers, json=data)
        
        # Check the response
        if response.status_code == 200:
            logger.info("Successfully sent the request!")
            logger.info(response.json())
        else:
            logger.info(f"Failed to send the request. Status code: {response.status_code}")
            logger.info(response.text)



@bot.event
async def on_disconnect():
    logger.info("Bot disconnected. Saving data...")

bot.run(TOKEN)
