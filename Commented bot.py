# Import all required libraries
import asyncio
import discord
import os
from discord.ext import commands
import time
from discord.message import Message

# Set a shorter name to be used often
client = commands.Bot(command_prefix = '_')

# When the bot is online...
@client.event
async def on_ready():
    # Change the activity to "Listening to DMs!"
    await client.change_presence(activity = discord.Activity(type=discord.ActivityType.listening, name='DMs!'))
    # Output to terminal
    print('Bot is ready!')

# When there is a command error...
@client.event
async def on_command_error(ctx, error):
    # More specifically, when the command is only able to be used in DMs (basically all cmds)
    if isinstance(error, commands.PrivateMessageOnly):
        try:
            # Inform the user of this
            await ctx.send(f'DM me to use commands {ctx.author.mention}!')
        except discord.HTTPException:
            pass


# Simple command to check the ping of the bot (and ensure it's online)
@client.command(aliases=['ping', 'p'])
async def pinggitypong(ctx):
    await ctx.send(f'**Latency:** {round(client.latency*1000, 1)}ms')
    print(f'Ping checked by {ctx.message.author.name}#{ctx.message.author.discriminator}.')

# A simple command to test the DM-only function of commands
@client.command()
@discord.ext.commands.dm_only()
async def pong(ctx):
    await ctx.send('Pong!')

# A 'say' command.
@client.command()
async def say(ctx, chnl, *speech):
    # Output channel to terminal (for debugging)
    print(chnl)
    # Check if the first argument is long enough for a channel to be mentioned
    if (len(chnl) <= 18) and (len(chnl) >= 21):
        # Tell the user to specify a channel
        await ctx.send('Please make sure you specify a channel!')
    else:
        # Get the channel they're mentioning
        channel = ctx.guild.get_channel(chnl)
        # Send the message (as a joined tuple) to the channel
        await channel.send(f'{" ".join(speech)}')

# A command to simply shut the bot down easier
@client.command(aliases=['goodnight', 'jaljjayo', 'sd'])
async def shutdown(ctx):
    # Checks if the user using the command is the bot owner (i.e. me)
    if str(ctx.message.author.id) != '221188745414574080':
        # If not, log it in terminal but don't respond to the user.
        print(f'{ctx.message.author} tried to shut the bot down lol')
    else:
        # Shut down
        await ctx.send('Shutting down...')
        exit()


# 'Report Bug' Command
@client.command()
async def rr(ctx):
    # Output to terminal (for debugging)
    print('Reporting started')
    # Define variables for a while loop to work
    ASteps = ""
    AExpected = ""
    AActual = ""
    AImage = ""
    print('MessageReply set to nothing')
    # Runs this script until they say "cancel" or until it finishes fully.
    while (ASteps.lower() != "cancel") or (AExpected.lower() != "cancel") or (AActual.lower() != "cancel") or (AImage.lower() != "cancel"):
        # Sends an embed informing about saying "cancel" and thanking them for their report.
        await ctx.send(embed=discord.Embed(color=discord.Color.from_rgb(59,214,198), title='Thanks for reporting a bug!', description='If at any time you wish to cancel (e.g. if the bog bugs and 2 embeds are sent), type `cancel`!\nIt may take until the image link submission for it to work though...'))
        # Sets the embed as a variable and sends it to the user
        QSteps = discord.Embed(color=discord.Color.from_rgb(59,214,198), title="Steps to reproduce:")
        await ctx.send(embed=QSteps)
        # Waits for a reply from the user
        MessageReply = await client.wait_for('message')
        # Adds it to a variable "Answer Steps"
        ASteps = (MessageReply.content)
        # Repeat
        QExpected = discord.Embed(color=discord.Color.from_rgb(59,214,198), title="Expected result:")
        await ctx.send(embed=QExpected)
        MessageReply = await client.wait_for("message")
        AExpected = (MessageReply.content)
        QActual = discord.Embed(color=discord.Color.from_rgb(59,214,198), title="Actual result:")
        await ctx.send(embed=QActual)
        MessageReply = await client.wait_for("message")
        AActual = (MessageReply.content)
        # Requests an image link (to be used in an embed)
        QImage = discord.Embed(color=discord.Color.from_rgb(59,214,198), title="Image link:", description="Make sure it ends in `.png`, `.gif`, or `.jpg` (change jpeg to jpg)! If no images, type `none`!\nRemember, you can only attach one image. If you need multiple please compile them into a single image.")
        await ctx.send(embed=QImage)
        MessageReply = await client.wait_for("message")
        AImage = (MessageReply.content)
        # Validation that the link is valid
        while (AImage[:7] != "https://") and (AImage[-4:] != ".png") and (AImage[-4:] != ".jpg") and (AImage[-4:] != ".gif") and (AImage.lower() != "none") and (AImage.lower() != "cancel"):
            if (AImage[:7] != "https://") and (AImage[-4:] != ".png") and (AImage[-4:] != ".jpg") and (AImage[-4:] != ".gif") and (AImage.lower() != "none") and (AImage.lower() != "cancel"):
                await ctx.send('Invalid link!') 
                # Requests a reply until it is valid or they say "none" or "cancel"
                MessageReply = await client.wait_for("message")
                AImage = (MessageReply.content)
        # Creates an embed for the user to ensure they typed everything correctly
        ECheck = discord.Embed(title="Bug Report", description="Please check the contents below to make sure everything is typed properly!", color=discord.Color.from_rgb(59,214,198))
        ECheck.add_field(name="**Steps to reproduce:**", value=f"{ASteps}", inline=False)
        ECheck.add_field(name="**Expected result:**", value=f"{AExpected}", inline=False)
        ECheck.add_field(name="**Actual result:**", value=f"{AActual}", inline=False)
        # Checks if the value given is a link or not to ensure the embed isn't formatted incorrectly and thus not sent
        if AImage.lower() == "none":
            pass
        else:
            ECheck.add_field(name="**Image links:**", value=f"{AImage}", inline=False)
            ECheck.set_image(url=f'{AImage}')
        # Sets footer with user information
        ECheck.set_footer(text=f'{ctx.author} ({ctx.author.id})')
        DMEmbed = await ctx.send(embed=ECheck)
        # Adds reactions for the user to let the bot know what happened
        await DMEmbed.add_reaction('✅')
        await DMEmbed.add_reaction('❌')
        print('Adds both reactions')
        # Waiting for the user to react (with a maximum of 1 minute)
        try:
            reaction, user = await client.wait_for('reaction_add', check=lambda reaction, user: user == ctx.author,  timeout = 60.0)
        except asyncio.TimeoutError:
            # If a minute passes with no reaction, log in terminal and inform the user that they need to start again.
            print(f'A bug report by {ctx.message.author.name}#{ctx.message.author.discriminator} timed out.')
            return await ctx.send('Validation timed out. Please try again.')
        else:
            # Checks what reaction we got
            if reaction.emoji == '✅':
                # The code will proceed to go through sending the embed to a checking channel, with a 2 day timeout (pls be quick) for reactions.
                # If it times out it will inform the user that "An error occured." and for them to resubmit their report
                await ctx.send("Thanks for the report! It's been sent to the Minju Managers to check it!")
                # Get the checking channel
                checkingchnl = ctx.guild.get_channel(842070840929419284)
                # Send the same embed (with a different footer) (Notice the grammar; "everything is typed properly". No second person.) to the checking channel for Managers to read
                ECheck.set_footer(text=f'Reported by {ctx.author} ({ctx.author.id})')
                CHECKEmbed = await checkingchnl.send(f'New bug report from **{ctx.message.author}** ({ctx.message.author.mention}). React with ✅ or ❌!', embed=ECheck)
                # Add both reactions to the embed
                await CHECKEmbed.add_reaction('✅')
                await CHECKEmbed.add_reaction('❌')
                # Waiting for a manager to react (with a maximum of 2 days (172800 seconds) because idk if i can do without timeout)
                try:
                    reaction2, user2 = await client.wait_for('reaction_add', check=lambda reaction2, user2: user2 == ctx.author,  timeout = 172800.0)
                except asyncio.TimeoutError:
                    print(f'A bug report by {ctx.message.author.name}#{ctx.message.author.discriminator} timed out.')
                    return await ctx.send('Validation timed out. Please try again.')
                else:
                # Checks what reaction we got
                # If a ✅, message is be edited to include who approved the bug
                    if reaction2.emoji == '✅':
                        await checkingchnl.send(embed=discord.Embed(title="Bug Report", description=f'Bug reported [here]() has been approved by {user}!', color=discord.Color.from_rgb(59,214,198)))
                        # Informs original user that the bug has been approved
                        await ctx.send('Your bug has been approved and sent to <#842070860494929950>!')
                        knownchnl = client.get_channel(842070860494929950)
                        # Embed is reformatted for known channel, and is sent.
                        KEmbed = discord.Embed(title="Bug Report", description="React with ⬆️ if you can reproduce the bug, and ⬇️ if you can't!", color=discord.Color.from_rgb(59,214,198))
                        KEmbed.add_field(name="**Steps to reproduce:**", value=f"{ASteps}", inline=False)
                        KEmbed.add_field(name="**Expected result:**", value=f"{AExpected}", inline=False)
                        KEmbed.add_field(name="**Actual result:**", value=f"{AActual}", inline=False)
                        if AImage.lower() == "none":
                            pass
                        else:
                            KEmbed.add_field(name="**Image links:**", value=f"{AImage}", inline=False)
                            KEmbed.set_image(url=f'{AImage}') 
                        KNOWNEmbed = await knownchnl.send(embed=KEmbed)
                        # Reactions added to the embed for users to react if they can reproduce the embed
                        await KNOWNEmbed.add_reaction('⬆️')
                        await KNOWNEmbed.add_reaction('⬇️')
                        # Reporting ended
                        break

                # If a ❌, manager is prompted for a reason.
                # Key words will be available such as "known {link}", "card", or "fixed" which will give automated responses such as
                # "This bug is known! Upvote it at {link}",
                # "This is a card error which is not reported as a bug. Please check the channel for information on what to report and what not to report!", and
                # "This bug has been fixed. Thanks for reporting though!"
                # This reason is then sent back to the original user, "Your bug 'insert steps to reproduce' was denied. Reason: {insert reason}"
            elif reaction.emoji == '❌':
                # If they say it's not right, tell them to start again.
                return await ctx.send('Please try again!')
            else:
                # If they react with something else, tell them to start again (there is no reaction check in the "client.wait_for" because otherwise it doesn't work)
                print(f'asd{reaction}asd{reaction.emoji}asd')
                return await ctx.send(f'You reacted with {reaction}... start again.')
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MIGHT INCORPORATE EDITING FEATURE FOR GRAMMAR/PUNCTUATION EDITS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # If :speech_balloon:, react with ①, ②, and ③ to let moderator choose which section to edit.
            # Allow them to input their own text.
            # Ask them if they're sure. If not, do it again. They don't get a 3rd chance because I'm lazy at coding another fucking while loop with shitty indenting
            # Send new embed asking if they want more changes.✅, ❌.
            # ✅ = back to line 173 (maybe)
            # Published to #known-bugs
            # DM original user stating it's been added to #known-bugs + message link and inform them there's been a change with a before/after
        
    # This is outside of the while loop (the "while they don't say cancel")
    print('Reporting ended.')
    if (ASteps.lower() == "cancel") or (AExpected.lower() == "cancel") or (AActual.lower() == "cancel") or (AImage.lower() == "cancel"):
        # Checks if they said "cancel" to know whether to send a cancelled message or not.
        await ctx.send(embed= discord.Embed(color=discord.Color.from_rgb(59,214,198), title="Bug report has been cancelled."))
        print(f'Report cancelled by {ctx.author.name}#{ctx.author.discriminator}.')
    else:
        pass
    # End of reporting bugs.
    


# Run the bot
client.run('Token')