import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

# This is your bot's Token.
TOKEN = 'your_bot_token_here'

# This is the ID of the channel where you want to log the activity.
LOG_CHANNEL_ID = 123456789012345678  # Replace with your actual channel ID

# Set up the bot
intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent.
intents.messages = True  # Subscribe to the messages intent for message logs.
intents.message_content = True  # Subscribe to message content intent if your bot needs to read message content.

bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionary to keep track of logging states
logging_states = {
    'join': True,
    'leave': True,
    'ban': True,
    'unban': True,
    'message_delete': True,
    'message_edit': True
}

# Dictionary to store open tickets
tickets = {}

@bot.command(name='openticket', help='Open a new support ticket.')
async def open_ticket(ctx):
    if ctx.author.id not in tickets:
        # Create a new text channel for the ticket
        channel = await ctx.guild.create_text_channel(f'ticket-{ctx.author.id}')
        
        # Add the user to the ticket dictionary
        tickets[ctx.author.id] = channel.id

        # Send a message to the ticket channel
        await channel.send(f"Ticket opened by {ctx.author.mention}. Support will be with you shortly.")

        # Log the ticket creation in the log channel
        if logging_states['message_edit']:
            await log_channel.send(f"Ticket opened by {ctx.author.display_name}. Channel: {channel.name}")

@bot.command(name='closeticket', help='Close your current support ticket.')
async def close_ticket(ctx):
    if ctx.author.id in tickets:
        # Get the ticket channel
        channel = bot.get_channel(tickets[ctx.author.id])

        # Delete the ticket channel
        await channel.delete()

        # Remove the ticket from the dictionary
        del tickets[ctx.author.id]

        # Log the ticket closure in the log channel
        if logging_states['message_edit']:
            await log_channel.send(f"Ticket closed by {ctx.author.display_name}. Channel: {channel.name}")
    else:
        await ctx.send("You don't have an open ticket.") 

# Event listener for when the bot has switched from offline to online.
@bot.event
async def on_ready():
    print(f'Bot is ready.')
    global log_channel
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    await log_channel.send('Bot is now online and ready to log server activity!')

# Event listener for when a member joins the server.
@bot.event
async def on_member_join(member):
    if logging_states['join']:
        await log_channel.send(f'{member.name} has joined the server.')

# Event listener for when a member leaves the server.
@bot.event
async def on_member_remove(member):
    if logging_states['leave']:
        await log_channel.send(f'{member.name} has left the server.')

# Event listener for when a member is banned from the server.
@bot.event
async def on_member_ban(guild, user):
    if logging_states['ban']:
        await log_channel.send(f'{user.name} has been banned from the server.')

# Event listener for when a member is unbanned from the server.
@bot.event
async def on_member_unban(guild, user):
    if logging_states['unban']:
        await log_channel.send(f'{user.name} has been unbanned from the server.')

# Event listener for when a message is deleted.
@bot.event
async def on_message_delete(message):
    if logging_states['message_delete']:
        await log_channel.send(f'A message by {message.author.display_name} was deleted in {message.channel}: {message.content}')

# Event listener for when a message is edited.
@bot.event
async def on_message_edit(before, after):
    if logging_states['message_edit']:
        await log_channel.send(f'A message by {before.author.display_name} was edited in {before.channel}.\nBefore: {before.content}\nAfter: {after.content}')

# Command to toggle logging features.
@bot.command(name='togglelog', help='Toggles logging features on and off.')
@has_permissions(administrator=True)
async def toggle_logging(ctx, feature: str):
    if feature in logging_states:
        logging_states[feature] = not logging_states[feature]
        state = 'on' if logging_states[feature] else 'off'
        await ctx.send(f'Logging for {feature} is now {state}.')
    else:
        await ctx.send('Invalid logging feature. Valid features are: join, leave, ban, unban, message_delete, message_edit.')

# Run the bot with the token
bot.run(TOKEN)
