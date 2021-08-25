import discord
from discord.ext import commands

class admincmds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @client.command(aliases=['goodnight', 'jaljjayo', 'sd', 'snowwhendubu', 'maliwhensunoo'])
    async def shutdown(ctx):
        if (ctx.message.author.id != '221188745414574080) and (ctx.message.author.id != 303901339891531779):
            print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: {ctx.message.author} tried to shut the bot down lol')
        else:
            print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Bot has been shut down.')
            await ctx.send('Shutting down...')
            await self.client.close()
            exit()

def setup(client):
    client.add_cog(admincmds(client))
