from discord.ext import commands

import discord

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Get the bot's latency.\n\nUsage: `ping`")
    async def ping(self, ctx):
        return await ctx.send(embed=discord.Embed(title="Pong!", description=f"Client latency: `{round(self.bot.latency * 1000)}ms`", color=0x45B6FE))

    @commands.command(help="Set the bot's status.\n\nUsage: `status <new_status>`")
    @commands.is_owner()
    async def status(self, ctx, *, new_status = None):
        if not new_status:
            return await ctx.send(embed=discord.Embed(title="Status", description=f"The bot status is currently: `{self.bot.status}`", color=0x45B6FE))
        await self.bot.update_status(new_status)        
        return await ctx.send(embed=discord.Embed(title="Status", description=f"The bot status has been updated to `{new_status}`", color=0x45B6FE))

    @commands.command(aliases=['user'])
    async def userinfo(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        embed = discord.Embed(title=f"User Info", color=0x45B6FE)
        embed.add_field(name="Username", value=user, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Account Created", value=user.created_at.strftime("%m/%d/%Y %H:%M:%S"), inline=False)
        if ctx.guild:
            embed.add_field(name="Joined Server", value=user.joined_at.strftime("%m/%d//%Y %H:%M:%S"), inline=False)
        embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
        return await ctx.send(embed=embed)

        
        

async def setup(bot):
    await bot.add_cog(General(bot))
