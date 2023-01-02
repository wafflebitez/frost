from discord.ext import commands

import discord, time

class Channels(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['dm'], help="Edit the Daily Message settings.\n\nUsage: `dailymessage <enable/disable/setchannel/removecooldown> [channel/user]`")
    @commands.guild_only()
    async def dailymessage(self, ctx, subcommand = None, arg = None):

        if not self.bot.servers[ctx.guild.id].is_mod(ctx.author):
            return await ctx.send(embed=discord.Embed(title="Error", description="You do not have permission to use this command.", color=0xDC143C))
        
        if not subcommand:
            embed = discord.Embed(title="Daily Message Settings", color=0x50C878)
            embed.add_field(name="Enabled", value="Yes" if self.bot.servers[ctx.guild.id].daily_message.enabled else "No", inline=False)
            embed.add_field(name="Channel", value=f"<#{self.bot.servers[ctx.guild.id].daily_message.channel_id}>" if self.bot.servers[ctx.guild.id].daily_message.channel_id else "None")
            embed.add_field(name="Cooldowns", value=len(self.bot.servers[ctx.guild.id].daily_message.cooldowns))
            return await ctx.send(embed=embed)

        subcommand = subcommand.lower()

        if subcommand == "enable":
            self.bot.servers[ctx.guild.id].daily_message.toggle(True)
            return await ctx.send(embed=discord.Embed(title="Success", description="Daily message enabled.", color=0x50C878))

        elif subcommand == "disable":
            self.bot.servers[ctx.guild.id].daily_message.toggle(False)
            self.bot.servers[ctx.guild.id].save()
            await ctx.send(embed=discord.Embed(title="Success", description="Daily message disabled.", color=0x50C878))

        elif subcommand == "setchannel":
            if not arg:
                return await ctx.send(embed=discord.Embed(title="Error", description="Please mention a channel.", color=0xDC143C))

            channel: discord.TextChannel
            try:
                channel = await commands.TextChannelConverter().convert(ctx, arg)
            except commands.BadArgument:
                channel = None

            if channel:
                self.bot.servers[ctx.guild.id].daily_message.set_channel(channel)
                return await ctx.send(embed=discord.Embed(title="Success", description="Daily message channel set.", color=0x50C878))
            
            return await ctx.send(embed=discord.Embed(title="Error", description="Invalid channel.", color=0xDC143C))

        elif subcommand == "removecooldown":
            if not arg:
                return await ctx.send(embed=discord.Embed(title="Error", description="Please mention a user.", color=0xDC143C))

            user: discord.Member
            try:
                user = await commands.MemberConverter().convert(ctx, arg)
            except commands.BadArgument:
                user = None

            if user:
                if self.bot.servers[ctx.guild.id].daily_message.remove_cooldown(user):
                    return await ctx.send(embed=discord.Embed(title="Success", description="Cooldown removed.", color=0x50C878))
                return await ctx.send(embed=discord.Embed(title="Error", description="User does not have a cooldown.", color=0xDC143C))
            return await ctx.send(embed=discord.Embed(title="Error", description="Invalid user.", color=0xDC143C))

        else:
            embed=discord.Embed(title="Error", description="Invalid subcommand.", color=0xDC143C)
            embed.add_field(name="Subcommands", value="`enable`, `disable`, `setchannel #channel`, `removecooldown @user`")
            await ctx.send(embed=embed)

    @commands.Cog.listener(name="on_message")
    async def on_daily_message(self, ctx):
        if (not ctx.guild or ctx.author.bot or not self.bot.servers[ctx.guild.id].daily_message.enabled or ctx.channel.id != self.bot.servers[ctx.guild.id].daily_message.channel_id):
            return

        if self.bot.servers[ctx.guild.id].daily_message.add_cooldown(ctx.author.id):
            embed = discord.Embed(title="Daily Message", description=f"You have sent your daily message in **{ctx.guild.name}**", color=0x45B6FE)
            embed.add_field(name="Message", value=ctx.content)
            if ctx.attachments:
                embed.add_field(name="Attachments", value="\n".join([f"[{a.filename}]({a.url})" for a in ctx.attachments]), inline=False)
            embed.set_footer(text=f"You can send your next message on {time.strftime('%A, %B %d, %Y at %I:%M %p', time.localtime(self.bot.servers[ctx.guild.id].daily_message.cooldowns[ctx.author.id]) + 86400)}")
            return await ctx.author.send(embed=embed)
        return await ctx.delete()
        
        

async def setup(bot):
    await bot.add_cog(Channels(bot))