import discord
import os
from datetime import datetime
from discord.ext import commands

class admincmds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def load(self, ctx, module : str):
        try:
            self.client.load_extension(f'rewrite.cogs.{module}')
        except Exception as e:
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('Loaded cog.')

    @commands.command()
    async def unload(self, ctx, module : str):
        try:
            self.client.unload_extension(f'rewrite.cogs.{module}')
        except Exception as e:
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('Unloaded cog.')

    @commands.command(aliases=['reload'])
    async def _reload(self, ctx, module : str):
        try:
            self.client.unload_extension(f'rewrite.cogs.{module}')
            self.client.load_extension(f'rewrite.cogs.{module}')
        except Exception as e:
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('Successfully reloaded cog.')


    @commands.command()
    async def restart(self, ctx):
        if ctx.author.id != 221188745414574080:
            pass
        else:
            await ctx.send("Restarting bot...")
            os.execv('python bot.py')

    @commands.command(aliases=['goodnight', 'jaljjayo', 'sd', 'snowwhendubu', 'maliwhensunoo'])
    async def shutdown(self, ctx):
        if (ctx.message.author.id != 221188745414574080) and (ctx.message.author.id != 303901339891531779):
            print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: {ctx.message.author} tried to shut the bot down lol')
        else:
            print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}::: Bot has been shut down.')
            await ctx.send('Shutting down...')
            await self.client.close()
            exit()

def setup(client):
    client.add_cog(admincmds(client))
