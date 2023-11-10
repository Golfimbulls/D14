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
