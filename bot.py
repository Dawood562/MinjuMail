import asyncio
import discord
import os
import json
import random
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands import errors
from discord.message import Message
# from discord_slash import SlashCommand
# from discord_slash.utils.manage_commands import create_option, create_choice
from datetime import datetime
# from collections import namedtuple
import traceback
import sys

#### JSON Functions ####
def add_vote(artist: str, gender: str, type: str):
    if os.path.isfile("suggestCards.json"):
        # Opens file and loads the data.
        with open("suggestCards.json", "r") as votes:
            data = json.load(votes)
        # Adds points if group already exists.
        try:
            data[f"{artist}"]["votes"] += 1
        # Creates a new group and adds points if group doesnt exist
        except KeyError:
            data[f"{artist}"] = {"artist":artist, "gender":gender, "atype":type, "votes": 1}
    else:
        data = {f"{artist}": {"points": 1}}
    # Saves file to store the data.
    with open("suggestCards.json", "w+") as votes:
        json.dump(data, votes, sort_keys=True, indent=4)


def get_votes(artist: str):
    with open("suggestCards.json", "r") as votes:
        data = json.load(votes)
    return data[f"{artist}"]["votes"]

def remove_artist(artist: str):
    if os.path.isfile("suggestCards.json"):
        # Opens file and loads the data.
        with open("suggestCards.json", "r") as votes:
            data = json.load(votes)
        try:
            for i in data:
                if data[i]["artist"].lower() == artist.lower():
                    # If found
                    data.pop(i)
                    print(data)
                    break
                else:
                    # If not found
                    pass
            json.dump(data, open("suggestCards.json", "w+"), indent=4)
        except KeyError:
            print("That group doesn't exist!")
        else:
            pass
#### JSON Functions ####

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '_', intents=intents, help_command=None, allowed_mentions = discord.AllowedMentions(everyone = False, roles = False))
# slash = SlashCommand(client, sync_commands=True)
# Wonyoung, Sakura, Yuri, Yena, Yujin, Nako, Eunbi, Hyewon, Hitomi, Chaewon, Minju, Chaeyeon
embedcolours = [discord.Color.from_rgb(217,89,140), discord.Color.from_rgb(241,210,231), discord.Color.from_rgb(243,170,81), discord.Color.from_rgb(252,246,149), discord.Color.from_rgb(86,122,206), discord.Color.from_rgb(183,211,233), discord.Color.from_rgb(187,176,220), discord.Color.from_rgb(219,112,108), discord.Color.from_rgb(241,195,170), discord.Color.from_rgb(206,229,213), discord.Color.from_rgb(254,254,254), discord.Color.from_rgb(167,224,225)]
helplist = [['reportabug', '**DM-ONLY:** Allows the user to report a bug!', '`bugreport`, `reportabug`, `reportbug`, `rab`, `rb`'], ['snow', 'Who knows?', '`snow`'], ['help', 'Displays the help message with all of the commands!', '`help`, `h`'], ['say', '**DEV-ONLY:** Lets the bot say something in a channel!', '`say`'], ['shutdown', '**DEV-ONLY:** Shuts the bot down.', '`shutdown`, `sd`, `jaljjayo`, `snowwhendubu`, `maliwhensunoo`'], ['ping', "Checks the bot's latency.", '`ping`, `p`'], ['pong', '**DM-ONLY:** Make the bot say "Pong"! Made to test DM-Only commands.', '`pong`'], ['bugreport', '**DM-ONLY:** Allows the user to report a bug!', '`bugreport`, `reportabug`, `reportbug`, `rab`, `rb`'], ['reportbug', '**DM-ONLY:** Allows the user to report a bug!', '`bugreport`, `reportabug`, `reportbug`, `rab`, `rb`'], ['rb', '**DM-ONLY:** Allows the user to report a bug!', '`bugreport`, `reportabug`, `reportbug`, `rab`, `rb`'], ['rab', '**DM-ONLY:** Allows the user to report a bug!', '`bugreport`, `reportabug`, `reportbug`, `rab`, `rb`']]
staffids = [389897179701182465, 221188745414574080, 303901339891531779, 257900648618655746, 193962293342502912, 364045258004365312, 297278578435948545]


@client.event
async def on_ready():
    await client.change_presence(activity = discord.Activity(type=discord.ActivityType.listening, name='DMs!'))
    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Bot is ready!')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.PrivateMessageOnly):
        try:
            await ctx.send(f'DM me to use commands {ctx.author.mention}!')
            await client.get_user(ctx.author.id).send('Use this channel to send me commands!')
        except discord.HTTPException:
            pass
    elif isinstance(error, commands.CommandOnCooldown):
        try:
            tleft = float(f'{error.retry_after:.2f}')
            minsleft = int(tleft//60)
            sleft = round(tleft%60, 2)
            if minsleft == 0:
                tlstring = f'{sleft} seconds'
            elif minsleft == 1 and sleft == 1:
                tlstring = f'1 minute **and** 1 second'
            elif minsleft == 1:
                tlstring = f'1 minute **and** {sleft} seconds'
            elif sleft == 1:
                tlstring = f'{minsleft} minutes and 1 second'
            else:    
                tlstring = f'{minsleft} minutes **and** {sleft} seconds'
            await ctx.send(f"You're on cooldown for another **{tlstring}** {ctx.author.mention}!")
        except discord.HTTPException:
            pass        
    else:
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

@client.command()
async def snow(ctx):
    await ctx.send("It's snowing! 🌨️")

@client.command(aliases=['h'])
async def help(ctx, *hargs):
    hargs = ''.join(hargs)
    if str(ctx.message.author.id) == '364045258004365312':
        HelpMessage = await ctx.send("lol aimi you shouldn't need help you code for a living smh")
    elif str(ctx.message.author.id) == '389897179701182465':
        HelpMessage = await ctx.send("i'm not helping you gary <:daepfft:796354212938121257>")
    elif hargs == '':
        HelpEmbed=discord.Embed(title='Help for MinjuMail!', description='This message will self-destruct in 1 minute so as to not take up too much space.', color=random.choice(embedcolours))
        HelpEmbed.add_field(name="Admin", value="say\nshutdown", inline=True)
        HelpEmbed.add_field(name="Utility", value="reportabug", inline=True)
        HelpEmbed.add_field(name="Miscellaneous", value="ping\npong\nsnow", inline=True)
        HelpMessage = await ctx.send(embed=HelpEmbed)
    else:
        found = False
        for i in helplist:
            if i[0] == f'{hargs}':
                index = helplist.index(i)
                found = True
                break
            else:
                pass
        if found == False:
            HelpMessage = await ctx.send(embed=discord.Embed(title='Misspelling?', description=f'I could not find {hargs} command in the list of commands {ctx.author.mention}!'))
        else:
            HelpEmbed=discord.Embed(title=f"Help for '{hargs}'!", description='', color=random.choice(embedcolours))
            HelpEmbed.add_field(name="Description", value=f'{helplist[index][1]}', inline=False)
            HelpEmbed.add_field(name="Aliases", value=f'{helplist[index][2]}', inline=False)
            HelpEmbed.add_field(name="Command example", value=f'_{helplist[index][0]}', inline=False)
        HelpMessage = await ctx.send(embed=HelpEmbed)
    await ctx.message.delete()
    await asyncio.sleep(60)
    await HelpMessage.delete()
        
@client.command()
async def plshelp(ctx, *hargs):
    hargs = ''.join(hargs)
    if (str(ctx.message.author.id) == '364045258004365312') or (str(ctx.message.author.id) == '389897179701182465'):
        if hargs == '':
            HelpEmbed=discord.Embed(title='Help for MinjuMail!', description='This message will self-destruct in 1 minute so as to not take up too much space.', color=random.choice(embedcolours))
            HelpEmbed.add_field(name="Admin", value="say\nshutdown", inline=True)
            HelpEmbed.add_field(name="Utility", value="reportabug", inline=True)
            HelpEmbed.add_field(name="Miscellaneous", value="ping\npong\nsnow", inline=True)
            HelpMessage = await ctx.send(embed=HelpEmbed)
        else:
            found = False
            for i in helplist:
                if i[0] == f'{hargs}':
                    index = helplist.index(i)
                    found = True
                    break
                else:
                    pass
            if found == False:
                HelpMessage = await ctx.send(embed=discord.Embed(title='Misspelling?', description=f'I could not find {hargs} command in the list of commands {ctx.author.mention}!'))
            else:
                HelpEmbed=discord.Embed(title=f"Help for '{hargs}'!", description='', color=random.choice(embedcolours))
                HelpEmbed.add_field(name="Description", value=f'{helplist[index][1]}', inline=False)
                HelpEmbed.add_field(name="Aliases", value=f'{helplist[index][2]}', inline=False)
                HelpEmbed.add_field(name="Command example", value=f'_{helplist[index][0]}', inline=False)
            HelpMessage = await ctx.send(embed=HelpEmbed)
        
        await ctx.message.delete()
        await asyncio.sleep(60)
        await HelpMessage.delete()
    else:
        pass

# @slash.slash(name='test1', description='Allows the user to report a bug', options=[create_option(name='stepstoreproduce',
#                description='What did you do to cause the bug?',
#                option_type=3,
#                required=True)])

# async def test1(ctx, steps: str):
#    await ctx.send(f'yes {steps}')


@client.command(aliases=['p'])
async def ping(ctx):
    await ctx.send(f'**Latency:** {round(client.latency*1000, 1)}ms')

@client.command()
@discord.ext.commands.dm_only()
async def pong(ctx):
    await ctx.send('Pong! This command can only be used in DMs! Cool, right?')

@client.command()
async def say(ctx, chnl, *speech):
    if (str(ctx.message.author.id) == '221188745414574080') or (str(ctx.message.author.id) == '303901339891531779'): 
        chnl = chnl.strip('<#>')
        channel = client.get_channel(int(chnl))
        await channel.send(f'{" ".join(speech)}')
        await chnl.send(f'{" ".join(speech)}')
    else:
        pass
    

@client.command()
async def accept(ctx, msgid: int):
    if ctx.author.id in staffids:
        asd = await client.get_channel(842070840929419284).fetch_message(msgid)
        if asd.embeds[0].title == 'Bug Report':            
            efields = asd.embeds[0].fields
            eauth = asd.embeds[0].author.name
            efooter = asd.embeds[0].footer.text
            steps = efields[0].value
            expected = efields[1].value
            actual = efields[2].value
            reporterid = int(efooter[efooter.find('(', 17, len(efooter))+1:-1])
            KEmbed = discord.Embed(title='Bug Report', description="React with ⬆️ if you've experienced this bug, and ⬇️ if you haven't!", color=random.choice(embedcolours))
            KEmbed.add_field(name="**Steps to Reproduce:**", value=f"{steps}", inline=False)
            KEmbed.add_field(name="**Expected result:**", value=f"{expected}", inline=False)
            KEmbed.add_field(name="**Actual result:**", value=f"{actual}", inline=False)
            if len(efields) == 4:
                KEmbed.add_field(name="**Image Link:**", value=f"{efields[3].value}", inline=False)
                KEmbed.set_image(url=f'{efields[3].value}')
            KEmbed.set_footer(text=f'{efooter}')
            KNOWNEmbed = await client.get_channel(842070860494929950).send(embed=KEmbed)
            await KNOWNEmbed.add_reaction('⬆️')
            await KNOWNEmbed.add_reaction('⬇️')
            await ctx.send(embed=discord.Embed(title='Bug Report Accepted', description=f'Bug report [here](https://discord.com/channels/774031288318296085/842070840929419284/{msgid}) has been approved by **{ctx.author}**, and <@{reporterid}> has been DMd.', color=random.choice(embedcolours)))
            await client.get_user(reporterid).send(embed=discord.Embed(title='Bug Report Accepted', description=f'[Your bug](https://discord.com/channels/@me/{eauth}) has been approved by **{ctx.author}** and sent to <#842070860494929950>.', color=random.choice(embedcolours)))
        else:
            efields = asd.embeds[0].fields
            eauth = asd.embeds[0].author.name
            efooter = asd.embeds[0].footer.text
            artist = efields[0].value
            gender = efields[1].value
            atype = efields[2].value
            VEmbed = discord.Embed(title='Card Suggestion', description='React with ⬆️ if you would like to see this artist in the game!')
            VEmbed.add_field(name="**Artist Name:**", value=f"{artist}", inline=False)
            VEmbed.add_field(name="**Artist Gender:**", value=f"{gender}", inline=False)
            VEmbed.add_field(name="**Artist Type:**", value=f"{atype}", inline=False)
            VEmbed.set_footer(text=f'{efooter}')
            SUGGESTEmbed = await client.get_channel(842070860494929950).send(embed=VEmbed)
            await SUGGESTEmbed.add_reaction('⬆️')
            await ctx.send(embed=discord.Embed(title='Card Suggestion Accepted', description=f'Card suggestion [here](https://discord.com/channels/774031288318296085/842070840929419284/{msgid}) has been approved by **{ctx.author}**.', color=random.choice(embedcolours)))
            await client.get_user(reporterid).send(embed=discord.Embed(title='Card Suggestion Accepted', description=f'[Your bug](https://discord.com/channels/@me/{eauth}) has been approved by **{ctx.author}** and sent to <#737721977816743966>.', color=random.choice(embedcolours)))
    else:
        await ctx.send(f'You need to be staff to use this {ctx.author.mention}!')

@client.command(aliases=['deny'])
async def reject(ctx, msgid: int):
    if ctx.author.id in staffids:
        asd = await client.get_channel(842070840929419284).fetch_message(msgid)
        eauth = asd.embeds[0].author.name
        efooter = asd.embeds[0].footer.text
        reporterid = int(efooter[efooter.find('(', 17, len(efooter))+1:-1])
        rejectreason = await client.get_channel(842070840929419284).send(embed=discord.Embed(title='Why are you rejecting this?', 
                                                    description='''Below are a list of keywords you can use:\n
                                                    __Bugs:__
                                                    **known (link)** - Sends a message saying that the bug is known and has been reported at `link`.
                                                    **card** - Informs the user that it's a card bug and so isn't accepted
                                                    **fixed** - Informs the user that by the time they reported the bug and we've seen it, it's already been fixed.

                                                    __Cards:__
                                                    **suggested** - Sends a message saying that the artist has already been suggested.
                                                    **info** - Sends a message saying that their suggestion contains incorrect information.

                                                    **troll** - Doesn't send a response because they're trolling with the submission.
                                                    ''', color=random.choice(embedcolours)))
        MessageReply = await client.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
        reason = (MessageReply.content)
        if reason[:5].lower() == 'known': 
            reason = f'This bug is already known! Please upvote it [here]({reason[6:]}).'
        elif reason.lower() == 'card':
            reason = 'This is a card error which is not reported as a bug. Please check the channel for information on what to report and what not to report!'
        elif reason.lower() == 'fixed':
            reason = 'Thanks for the report, but by the time a Minju Manager had gotten to it the bug had already been fixed.'
        elif reason.lower() == 'suggested':
            reason = 'Thanks for the suggestion, but this is already in the channel! Please check next time!'
        elif reason.lower() == 'info':
            reason = 'Thanks for your suggestion, but the information you provided is incorrect!'
        else:
            pass
        if reason == 'troll':
            pass
        else:
            await MessageReply.delete()
            await rejectreason.edit(embed=discord.Embed(title=f'{asd.embeds[0].title} successfully rejected!', description=f'{asd.embeds[0].title} [here](https://discord.com/channels/774031288318296085/842070840929419284/{msgid}) has successfully been rejected by **{ctx.author}**, and <@{reporterid}> has been DMd. Reason:\n\n> {reason}', color=random.choice(embedcolours)))
            await client.get_user(reporterid).send(embed=discord.Embed(title=f'Your {asd.embeds[0].title} has been rejected.', description=f'[Your {asd.embeds[0].title}](https://discord.com/channels/@me/{eauth}) was rejected by {ctx.author}.\n\nReason:\n> {reason}', color=random.choice(embedcolours)))
    else:
        await ctx.send(f'You need to be staff to use this {ctx.author.mention}!')

@client.command(aliases=['goodnight', 'jaljjayo', 'sd', 'snowwhendubu', 'maliwhensunoo'])
async def shutdown(ctx):
    if (str(ctx.message.author.id) != '221188745414574080') and (str(ctx.message.author.id) != '303901339891531779'):
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: {ctx.message.author} tried to shut the bot down lol')
    else:
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Bot has been shut down.')
        await ctx.send('Shutting down...')
        await client.close()
        exit()


@client.command()
@commands.cooldown(1,5,commands.BucketType.user)
async def points(ctx, *type):
    try:
        print(getvotes(type))
    except KeyError:
        await ctx.send(f'{ctx.author.mention}, {type} has never been suggested.')
    else:
        novotes = getvotes(type)
        await ctx.send(f'{ctx.author.mention}, {type} has {novotes} votes.')
        
        

@client.command()
@discord.ext.commands.dm_only()
@commands.cooldown(1,900,commands.BucketType.user)
async def testcd(ctx):
    await ctx.send('15 minute cooldown now lol')


@client.command(aliases=['bugreport', 'br', 'reportbug', 'rab', 'rb'])
@discord.ext.commands.dm_only()
@commands.cooldown(1,900,commands.BucketType.user)
async def reportabug(ctx):
    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Reporting started by {ctx.message.author}')
    while True:
        await ctx.send(embed=discord.Embed(color=random.choice(embedcolours), title='Thanks for reporting a bug!', description='If at any time you wish to cancel (e.g. if the bog bugs and 2 embeds are sent), type `cancel`!\nIt may take until the image link submission for it to work though...'))
        QSteps = discord.Embed(color=random.choice(embedcolours), title="Steps to reproduce:")
        await ctx.send(embed=QSteps)
        MessageReply = await client.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
        ASteps = (MessageReply.content)
        # Check to cancel
        if ASteps.lower() == "cancel":
            break
        else:
            pass
        ##################
        QExpected = discord.Embed(color=random.choice(embedcolours), title="Expected result:")
        await ctx.send(embed=QExpected)
        MessageReply = await client.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
        AExpected = (MessageReply.content)
        # Check to cancel
        if AExpected.lower() == "cancel":
            break
        else:
            pass
        ##################
        QActual = discord.Embed(color=random.choice(embedcolours), title="Actual result:")
        await ctx.send(embed=QActual)
        MessageReply = await client.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
        AActual = (MessageReply.content)
        # Check to cancel
        if AActual.lower() == "cancel":
            break
        else:
            pass
        ##################
        QImage = discord.Embed(color=random.choice(embedcolours), title="Image:", description="Make sure it ends in `.png`, `.gif`, or `.jpg`! If no images, type `none`!\nRemember, you can only attach one image. If you need multiple please compile them into a single image.\nIf you send an attachment please make sure you don't delete the message, else the link will become invalid.\nIf you send both an attachment and an image link, only the attachment will be taken.")
        await ctx.send(embed=QImage)
        MessageReply = await client.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
        AImage = (MessageReply.content)
        # Taking image or link
        result = None
        while result is None:
            try:
                AImage = MessageReply.attachments[0].url
                if AImage[:7] != "https://" and AImage[-4:] != ".png" and AImage[-4:] != ".jpg" and AImage[-4:] != ".jpeg" and AImage[-4:] != ".gif":
                    await ctx.send('The image needs to be a `.gif`, `.png`, or `.jpg`!') 
                    MessageReply = await client.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
                    AImage = (MessageReply.content)
                else:
                    result = True
                ECheck = discord.Embed(title="Bug Report")
                ECheck.set_image(url=f'{AImage}')
                DMEmbed = await ctx.send(embed=ECheck)
            except IndexError:
                if ((AImage[:7] != "https://") and (AImage[-4:] != ".png" and AImage[-4:] != ".jpg" and AImage[-5:] != ".jpeg" and AImage[-4:] != ".gif")) and AImage.lower() != "none" and AImage.lower() != "cancel":
                    await ctx.send('Invalid link!') 
                    MessageReply = await client.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
                    AImage = (MessageReply.content)
                else:
                    result = True
            else:
                break
        # Check to cancel
        if AImage.lower() == "cancel":
            break
        else:
            pass
        ##################
        ECheck = discord.Embed(title="Bug Report", description="Please check the contents below to make sure everything is typed properly!", color=random.choice(embedcolours))
        ECheck.add_field(name="**Steps to reproduce:**", value=f"{ASteps}", inline=False)
        ECheck.add_field(name="**Expected result:**", value=f"{AExpected}", inline=False)
        ECheck.add_field(name="**Actual result:**", value=f"{AActual}", inline=False)
        if AImage.lower() == "none":
            pass
        else:
            ECheck.add_field(name="**Image links:**", value=f"{AImage}", inline=False)
            ECheck.set_image(url=f'{AImage}')
        ECheck.set_footer(text=f'{ctx.author} ({ctx.author.id})')
        DMEmbed = await ctx.send(embed=ECheck)
        await DMEmbed.add_reaction('❌')
        await DMEmbed.add_reaction('✅')
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Adds both reactions')
        try:
            reaction, user = await client.wait_for('reaction_add', check=lambda reaction, user: user == ctx.author,  timeout = 60.0)
        except asyncio.TimeoutError:
            print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: A bug report by {ctx.message.author} timed out.')
            return await ctx.send('Validation timed out. Please try again.')
        else:
            if reaction.emoji == '✅':
                await ctx.send("Thanks for the report! It's been sent to the Minju Managers to check it! Expect a reply within 2 days :)")
                await DMEmbed.remove_reaction('❌', client.user)
                await DMEmbed.remove_reaction('✅', client.user)
                
                ECheck.set_footer(text=f'Suggested by {ctx.author} ({ctx.author.id})')
                ECheck.set_author(name=f'{ctx.message.channel.id}/{DMEmbed.id}')
                CHECKEmbed = await client.get_channel(842070840929419284).send(f"New bug report from **{ctx.message.author}** ({ctx.message.author.mention}).", embed=ECheck)
                await CHECKEmbed.edit(content=f"New bug report from **{ctx.message.author}** ({ctx.message.author.mention}).\nUse `_accept {CHECKEmbed.id}` or `_reject {CHECKEmbed.id}` to accept or reject this bug report.", embed=ECheck)
                print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Bug report by {ctx.message.author} has been sent to the checking channel.')
            elif reaction.emoji == '❌':
                # Remove all reactions
                CLDEmbed = discord.Embed(title='Bug Report has been cancelled.', description='Please reuse the command to redo your entries!', color=random.choice(embedcolours))
                await DMEmbed.edit(embed=CLDEmbed)
                await DMEmbed.remove_reaction('❌', client.user)
                await DMEmbed.remove_reaction('✅', client.user)
                print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Bug report by {ctx.message.author} has been cancelled.')

            else:
                return await ctx.send(f'You reacted with {reaction}... start again.')
            
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MIGHT INCORPORATE EDITING FEATURE FOR GRAMMAR/PUNCTUATION EDITS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # If :speech_balloon:, react with ①, ②, and ③ to let moderator choose which section to edit.
            # Allow them to input their own text.
            # Ask them if they're sure. If not, do it again. They don't get a 3rd chance because I'm lazy at coding another fucking while loop with shitty indenting
            # Send new embed asking if they want more changes.✅, ❌.
            # ✅ = back to line 173 (maybe)
            # Published to #known-bugs
            # DM original user stating it's been added to #known-bugs + message link and inform them there's been a change with a before/after
            # nah just make an edit command
        break
    # This is outside of the while loop (the "while they don't say cancel")
    print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}::: {ctx.author}'s report ended.")
    if (ASteps.lower() == "cancel") or (AExpected.lower() == "cancel") or (AActual.lower() == "cancel") or (AImage.lower() == "cancel"):
        # Checks if they said "cancel" to know whether to send a cancelled message or not.
        await ctx.send(embed= discord.Embed(color=random.choice(embedcolours), title="Bug report has been cancelled."))
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: A report by {ctx.message.author} has been cancelled.')
    else:
        pass

@reportabug.error
async def clear_error(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send("Please send a valid link/image, not just some text!\n\n*You're going to have to restart the command.*")
    else:
        await ctx.send('An unexpected error occured. Please try again, and let DaSnow562#0562 know what went wrong!')

def checkgivenfield(newembed, EmbedToEdit, editing, givenfield):
    if givenfield.lower() == 'steps':
        newembed.add_field(name="**Steps to Reproduce:**", value=f"{editing}", inline=False)
        newembed.add_field(name="**Expected Result:**", value=f"{EmbedToEdit.embeds[0].fields[1].value}", inline=False)
        newembed.add_field(name="**Actual Result:**", value=f"{EmbedToEdit.embeds[0].fields[2].value}", inline=False)
        newembed.add_field(name="**Image Links:**", value=f"{EmbedToEdit.embeds[0].fields[3].value}", inline=False)
        newembed.set_image(url=f'{EmbedToEdit.embeds[0].fields[3].value}')
    if givenfield.lower() == 'expected':
        newembed.add_field(name="**Steps to Reproduce:**", value=f"{EmbedToEdit.embeds[0].fields[0].value}", inline=False)
        newembed.add_field(name="**Expected Result:**", value=f"{editing}", inline=False)
        newembed.add_field(name="**Actual Result:**", value=f"{EmbedToEdit.embeds[0].fields[2].value}", inline=False)
        newembed.add_field(name="**Image Links:**", value=f"{EmbedToEdit.embeds[0].fields[3].value}", inline=False)
        newembed.set_image(url=f'{EmbedToEdit.embeds[0].fields[3].value}')
    if givenfield.lower() == 'actual':
        newembed.add_field(name="**Steps to Reproduce:**", value=f"{EmbedToEdit.embeds[0].fields[0].value}", inline=False)
        newembed.add_field(name="**Expected Result:**", value=f"{EmbedToEdit.embeds[0].fields[1].value}", inline=False)
        newembed.add_field(name="**Actual Result:**", value=f"{editing}", inline=False)
        newembed.add_field(name="**Image Links:**", value=f"{EmbedToEdit.embeds[0].fields[3].value}", inline=False)
        newembed.set_image(url=f'{EmbedToEdit.embeds[0].fields[3].value}')
    else:
        newembed = 'no'
    return newembed


@client.command(aliases=['sac', 'scard', 'scards', 'cardsuggest', 'cs'])
@discord.ext.commands.dm_only()
@commands.cooldown(1,900,commands.BucketType.user)
async def suggestacard(ctx):
    print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Card Suggestion started by {ctx.message.author}')
    while True:
        await ctx.send(embed=discord.Embed(color=random.choice(embedcolours), title='Thanks for wanting to suggest an artist!', description='Please remember that this should only be used if the artist is not already in the game or in the <#737721977816743966> channel!\nIf at any time you wish to cancel (e.g. if the bog bugs and 2 embeds are sent), type `cancel`! It takes until the 3rd embed for it to cancel, however.'))
        QGroup = discord.Embed(color=random.choice(embedcolours), title="Artist Name (Without special characters):")
        await ctx.send(embed=QGroup)
        MessageReply = await client.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
        AArtist = (MessageReply.content)
        # Check to cancel
        if AArtist.lower() == "cancel":
            break
        else:
            pass
        ##################
        QGender = discord.Embed(color=random.choice(embedcolours), title='Artist Gender (Male, Female, or Mixed):')
        await ctx.send(embed=QGender)
        MessageReply = await client.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
        AGender = (MessageReply.content)
        # Check to cancel
        if AGender.lower() == "cancel":
            break
        else:
            pass
        ##################
        QType = discord.Embed(color=random.choice(embedcolours), title="Artist Type (Group/Soloist):")
        await ctx.send(embed=QType)
        MessageReply = await client.wait_for('message', check=lambda message: message.author.id == ctx.author.id)
        AType = (MessageReply.content)
        # Check to cancel
        if AType.lower() == "cancel":
            break
        else:
            pass
        ##################
        ECheck = discord.Embed(title="Card Suggestion", description="Please check the contents below to make sure everything is typed properly!", color=random.choice(embedcolours))
        ECheck.add_field(name="**Artist Name:**", value=f"{AArtist}", inline=False)
        ECheck.add_field(name="**Artist Gender:**", value=f"{AGender}", inline=False)
        ECheck.add_field(name="**Artist Type:**", value=f"{AType}", inline=False)
        ECheck.set_footer(text=f'{ctx.author} ({ctx.author.id})')
        DMEmbed = await ctx.send(embed=ECheck)
        await DMEmbed.add_reaction('❌')
        await DMEmbed.add_reaction('✅')
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Adds both reactions')
        try:
            reaction, user = await client.wait_for('reaction_add', check=lambda reaction, user: user == ctx.author,  timeout = 60.0)
        except asyncio.TimeoutError:
            print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: A card suggestion by {ctx.message.author} timed out.')
            return await ctx.send('Validation timed out. Please try again.')
        else:
            if reaction.emoji == '✅':
                await ctx.send("Thanks for the suggestion! It's been sent to the Minju Managers to verify the information!")
                await DMEmbed.remove_reaction('❌', client.user)
                await DMEmbed.remove_reaction('✅', client.user)
                
                ECheck.set_footer(text=f'Suggested by {ctx.author} ({ctx.author.id})')
                ECheck.set_author(name=f'{ctx.message.channel.id}/{DMEmbed.id}')
                CHECKEmbed = await client.get_channel(842070840929419284).send(f"New card suggestion from **{ctx.message.author}** ({ctx.message.author.mention}).", embed=ECheck)
                await CHECKEmbed.edit(content=f"New card suggestion from **{ctx.message.author}** ({ctx.message.author.mention}).\nUse `_accept {CHECKEmbed.id}` or `_reject {CHECKEmbed.id}` to accept or reject this card suggestion.\nAlso remember that they can't submit special characters so don't reject for that!", embed=ECheck)
                print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Card suggestion by {ctx.message.author} has been sent to the checking channel.')
                break
            elif reaction.emoji == '❌':
                # Remove all reactions
                CLDEmbed = discord.Embed(title='Card suggestion has been cancelled.', description='Please reuse the command to redo your entries!', color=random.choice(embedcolours))
                await DMEmbed.edit(embed=CLDEmbed)
                await DMEmbed.remove_reaction('❌', client.user)
                await DMEmbed.remove_reaction('✅', client.user)
                print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Card suggestion by {ctx.message.author} has been cancelled.')
                break

            else:
                return await ctx.send(f'You reacted with {reaction}... start again.')
                break


@client.command()
async def edit(ctx, msgid: int, givenfield: str, *editing):
    editing = ' '.join(editing)
    print(f'"{givenfield}"')
    print(f'"{givenfield.lower()}"')
    try:
        EmbedToEdit = await client.get_channel(842070860494929950).fetch_message(msgid)
    except discord.errors.NotFound:
        await ctx.send("That message cannot be found! Please make sure it's in <#842070860494929950>!")
    else:
        newembed = discord.Embed(title='Bug Report', description="React with ⬆️ if you've experienced this bug, and ⬇️ if you haven't!")
        newembed.set_footer(text=f'{EmbedToEdit.embeds[0].footer.text}')
        await ctx.send(f'Normal: "{givenfield}"\nLowercase: "{givenfield.lower()}"')
        try:
             link = EmbedToEdit.embeds[0].fields[3].value
        except IndexError:
            await ctx.send('No link found')
            newembed = checkgivenfield(newembed, EmbedToEdit, editing, givenfield)
            if newembed != 'no':
                await EmbedToEdit.edit(embed=newembed)
                confirmation = await ctx.send('Message has been edited!')
                await asyncio.sleep(10)
                await confirmation.delete()
                await ctx.message.delete()
            else:
                await ctx.send('You need to say one of `steps`, `expected`, or `actual`!')
        else:
            await ctx.send('Link found')
            newembed = checkgivenfield(newembed, EmbedToEdit, editing, givenfield)
            if newembed != 'no':
                await EmbedToEdit.edit(embed=newembed)
                confirmation = await ctx.send('Message has been edited!')
                await asyncio.sleep(10)
                await confirmation.delete()
                await ctx.message.delete()
            else:
                await ctx.send('You need to say one of `steps`, `expected`, or `actual`!')
    

client_token = os.environ.get("TOKEN")
client.run(client_token)
