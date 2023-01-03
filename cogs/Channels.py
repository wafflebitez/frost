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
            embed.add_field(name="Channel", value=f"<#{self.bot.servers[ctx.guild.id].daily_message.channel_id}>" if self.bot.servers[ctx.guild.id].daily_message.channel_id else "None", inline=False)
            embed.add_field(name="Cooldowns", value=len(self.bot.servers[ctx.guild.id].daily_message.cooldowns))
            embed.add_field(name="Subcommands", value="`enable`, `disable`, `setchannel #channel`, `removecooldown @user`", inline=False)
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
                self.bot.servers[ctx.guild.id].daily_message.set_channel(channel.id)
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

        embed = discord.Embed(title="Daily Message", description="Invalid subcommand.", color=0xDC143C)
        embed.add_field(name="Subcommands", value="`enable`, `disable`, `setchannel #channel`, `removecooldown @user`")
        await ctx.send(embed=embed)

    @commands.Cog.listener(name="on_message")
    async def on_daily_message(self, ctx):
        if (not ctx.guild or ctx.author.bot or not self.bot.servers[ctx.guild.id].daily_message.enabled or ctx.channel.id != self.bot.servers[ctx.guild.id].daily_message.channel_id or ctx.content.startswith(self.bot.servers[ctx.guild.id].prefix)):
            return

        if self.bot.servers[ctx.guild.id].daily_message.add_cooldown(ctx.author.id):
            embed = discord.Embed(title="Daily Message", description=f"You have sent your daily message in **{ctx.guild.name}**", color=0x45B6FE)
            embed.add_field(name="Message", value=ctx.content)
            if ctx.attachments:
                embed.add_field(name="Attachments", value="\n".join([f"[{a.filename}]({a.url})" for a in ctx.attachments]), inline=False)
            embed.set_footer(text=f"You can send your next message on {time.strftime('%A, %B %d, %Y at %I:%M %p', time.localtime(self.bot.servers[ctx.guild.id].daily_message.cooldowns[ctx.author.id]))}")
            return await ctx.author.send(embed=embed)
        return await ctx.delete()
        


    @commands.command(help="Edit the Counting settings.\n\nUsage: `counting <enable/disable/setchannel/setuser/setnumber/blacklist> [channel/number/user]`")
    @commands.guild_only()
    async def counting(self, ctx, subcommand = None, arg = None):
            if not self.bot.servers[ctx.guild.id].is_mod(ctx.author):
                return await ctx.send(embed=discord.Embed(title="Error", description="You do not have permission to use this command.", color=0xDC143C))
            
            if not subcommand:
                embed = discord.Embed(title="Counting Settings", color=0x50C878)
                embed.add_field(name="Enabled", value="Yes" if self.bot.servers[ctx.guild.id].counting.enabled else "No", inline=False)
                embed.add_field(name="Channel", value=f"<#{self.bot.servers[ctx.guild.id].counting.channel_id}>" if self.bot.servers[ctx.guild.id].counting.channel_id else "None", inline=False)
                embed.add_field(name="Number", value=self.bot.servers[ctx.guild.id].counting.number)
                embed.add_field(name="User", value=f"<@{self.bot.servers[ctx.guild.id].counting.last_user}>" if self.bot.servers[ctx.guild.id].counting.last_user != 0 else "None")
                embed.add_field(name="Blacklisted Users", value=f'<@{" @".join([str(u) for u in self.bot.servers[ctx.guild.id].counting.blacklist])}>' if self.bot.servers[ctx.guild.id].counting.blacklist else "None", inline=False)
                embed.add_field(name="Subcommands", value="`enable`, `disable`, `setchannel #channel`, `setuser @user`, `setnumber <number>`, `blacklist <add/remove> @user`", inline=False)
                return await ctx.send(embed=embed)
    
            subcommand = subcommand.lower()
    
            if subcommand == "enable":
                self.bot.servers[ctx.guild.id].counting.toggle(True)
                return await ctx.send(embed=discord.Embed(title="Counting", description="Counting enabled.", color=0x50C878))
    
            elif subcommand == "disable":
                self.bot.servers[ctx.guild.id].counting.toggle(False)
                self.bot.servers[ctx.guild.id].save()
                await ctx.send(embed=discord.Embed(title="Counting", description="Counting disabled.", color=0x50C878))
    
            elif subcommand == "setchannel":
                if not arg:
                    return await ctx.send(embed=discord.Embed(title="Counting", description="Please mention a channel.", color=0xDC143C))
    
                channel: discord.TextChannel
                try:
                    channel = await commands.TextChannelConverter().convert(ctx, arg)
                except commands.BadArgument:
                    channel = None
    
                if channel:
                    self.bot.servers[ctx.guild.id].counting.set_channel(channel.id)
                    return await ctx.send(embed=discord.Embed(title="Counting", description="Counting channel set.", color=0x50C878))
                return await ctx.send(embed=discord.Embed(title="Counting", description="Invalid channel.", color=0xDC143C))


            elif subcommand == "setnumber":
                if not arg:
                    return await ctx.send(embed=discord.Embed(title="Counting", description="Please enter a number.", color=0xDC143C))
                
                try:
                    number = int(arg)
                except ValueError:
                    return await ctx.send(embed=discord.Embed(title="Counting", description="Invalid number.", color=0xDC143C))

                self.bot.servers[ctx.guild.id].counting.set_number(number)
                return await ctx.send(embed=discord.Embed(title="Counting", description="Last number set.", color=0x50C878))

            elif subcommand == "setuser":
                if not arg:
                    return await ctx.send(embed=discord.Embed(title="Counting", description="Please mention a user.", color=0xDC143C))
    
                user: discord.User
                try:
                    user = await commands.UserConverter().convert(ctx, arg)
                except commands.BadArgument:
                    user = None
    
                if user:
                    self.bot.servers[ctx.guild.id].counting.set_last_user(user.id)
                    return await ctx.send(embed=discord.Embed(title="Counting", description="Last user set.", color=0x50C878))
                return await ctx.send(embed=discord.Embed(title="Counting", description="Invalid user.", color=0xDC143C))

            elif subcommand == "blacklist":
                if not arg:
                    return await ctx.send(embed=discord.Embed(title="Counting", description="Please mention a user.", color=0xDC143C))
    
                user: discord.User
                try:
                    user = await commands.UserConverter().convert(ctx, arg)
                except commands.BadArgument:
                    user = None
    
                if user:
                    if self.bot.servers[ctx.guild.id].counting.add_blacklist(user.id):
                        return await ctx.send(embed=discord.Embed(title="Counting", description="User blacklisted.", color=0x50C878))
                    return await ctx.send(embed=discord.Embed(title="Counting", description="User unblacklisted.", color=0x50C878))
                
                return await ctx.send(embed=discord.Embed(title="Counting", description="Invalid user.", color=0xDC143C))

            embed = discord.Embed(title="Counting", description="Invalid subcommand.", color=0xDC143C)
            embed.add_field(name="Subcommands", value="`enable`, `disable`, `setchannel #channel`, `setnumber 123`, `setuser @user`, `blacklist`")
            return await ctx.send(embed=embed)

    @commands.Cog.listener(name="on_message")
    async def on_counting_message(self, ctx):
        if (not ctx.guild or not self.bot.servers[ctx.guild.id].counting.enabled or ctx.channel.id != self.bot.servers[ctx.guild.id].counting.channel_id or ctx.author.bot or (ctx.content.startswith(self.bot.servers[ctx.guild.id].prefix) and self.bot.servers[ctx.guild.id].is_mod(ctx.author))):
            return

        try:
            number = int(ctx.content)
        except ValueError:
            await ctx.channel.send(embed=discord.Embed(title="Counting", description="Invalid number. Messages sent must be numbers only!", color=0xDC143C), delete_after=5)
            return await ctx.delete()
        
        result = self.bot.servers[ctx.guild.id].counting.increment(ctx.author.id, number)

        if result == 'blacklisted':
            await ctx.channel.send(embed=discord.Embed(title="Counting", description="You are blacklisted from counting.", color=0xDC143C), delete_after=5)
            return await ctx.delete()
        elif result == 'same_user':
            await ctx.channel.send(embed=discord.Embed(title="Counting", description="You cannot count twice in a row.", color=0xDC143C), delete_after=5)
            return await ctx.delete()
        elif result == 'wrong_number':
            await ctx.channel.send(embed=discord.Embed(title="Counting", description=f"That's the wrong number! The next number in the sequence is `{self.bot.servers[ctx.guild.id].counting.number + 1}`.", color=0xDC143C), delete_after=5)
            return await ctx.delete()

        return await ctx.add_reaction("✅")



    @commands.command(alias=["suggestion"])
    async def suggestions(self, ctx, subcommand = None, arg = None):
        if not self.bot.servers[ctx.guild.id].is_mod(ctx.author):
            return await ctx.send(embed=discord.Embed(title="Error", description="You do not have permission to use this command.", color=0xDC143C))

        if not subcommand:
            response = discord.Embed(title="Suggestions", color=0x50C878)
            response.add_field(name="Enabled", value="Yes" if self.bot.servers[ctx.guild.id].suggestions.enabled else "No", inline=False)
            response.add_field(name="Channel", value=f"<#{self.bot.servers[ctx.guild.id].suggestions.channel_id}>" if self.bot.servers[ctx.guild.id].suggestions.channel_id else "None", inline=False)
            response.add_field(name="Submitted Suggestions", value=len(self.bot.servers[ctx.guild.id].suggestions.suggestions), inline=False)
            response.add_field(name="Subcommands", value="`enable`, `disable`, `setchannel #channel`, `blacklist @user`", inline=False)
            return await ctx.send(embed=response)

        if subcommand == "enable":
            self.bot.servers[ctx.guild.id].suggestions.toggle(True)
            return await ctx.send(embed=discord.Embed(title="Suggestions", description="Suggestions enabled.", color=0x50C878))

        elif subcommand == "disable":
            self.bot.servers[ctx.guild.id].suggestions.toggle(False)
            return await ctx.send(embed=discord.Embed(title="Suggestions", description="Suggestions disabled.", color=0x50C878))

        elif subcommand == "setchannel":
            if not arg:
                return await ctx.send(embed=discord.Embed(title="Suggestions", description="Please mention a channel.", color=0xDC143C))
    
            channel: discord.TextChannel
            try:
                channel = await commands.TextChannelConverter().convert(ctx, arg)
            except commands.BadArgument:
                channel = None
    
            if channel:
                self.bot.servers[ctx.guild.id].suggestions.set_channel(channel.id)
                return await ctx.send(embed=discord.Embed(title="Suggestions", description="Channel set.", color=0x50C878))
            return await ctx.send(embed=discord.Embed(title="Suggestions", description="Invalid channel.", color=0xDC143C))

        elif subcommand == "blacklist":
            if not arg:
                return await ctx.send(embed=discord.Embed(title="Suggestions", description="Please mention a user.", color=0xDC143C))
    
            user: discord.User
            try:
                user = await commands.UserConverter().convert(ctx, arg)
            except commands.BadArgument:
                user = None
    
            if user:
                if self.bot.servers[ctx.guild.id].suggestions.add_blacklist(user.id):
                    return await ctx.send(embed=discord.Embed(title="Suggestions", description="User blacklisted.", color=0x50C878))
                return await ctx.send(embed=discord.Embed(title="Suggestions", description="User unblacklisted.", color=0x50C878))
            return await ctx.send(embed=discord.Embed(title="Suggestions", description="Invalid user.", color=0xDC143C))

        embed = discord.Embed(title="Suggestions", description="Invalid subcommand.", color=0xDC143C)
        embed.add_field(name="Subcommands", value="`enable`, `disable`, `setchannel #channel`, `blacklist @user`")
        return await ctx.send(embed=embed)

    @commands.Cog.listener(name="on_message")
    async def on_suggestion_message(self, ctx):
        if (not ctx.guild or not self.bot.servers[ctx.guild.id].suggestions.enabled or ctx.channel.id != self.bot.servers[ctx.guild.id].suggestions.channel_id or ctx.author.bot or (ctx.content.startswith(self.bot.servers[ctx.guild.id].prefix) and self.bot.servers[ctx.guild.id].is_mod(ctx.author))):
            return
        
        if not ctx.content and not ctx.attachments:
            return await ctx.delete()
            
        message = ctx.content
        if ctx.attachments:
            message += "\n"
            message += "\n".join(f"[{a.filename}]({a.url})" for a in ctx.attachments)
        result = self.bot.servers[ctx.guild.id].suggestions.add_suggestion(ctx.author.id, message)
        if not result:
            await ctx.delete()
            return await ctx.channel.send(embed=discord.Embed(title="Suggestions", description="You are blacklisted from submitting suggestions.", color=0xDC143C), delete_after=5)

        embed = discord.Embed(title="New Suggestion", description=message, color=0x50C878)
        embed.add_field(name="Submitted By", value=ctx.author.mention)
        embed.set_footer(text=f"Suggestion #{len(self.bot.servers[ctx.guild.id].suggestions.suggestions)}")
        await ctx.delete()
        message = await ctx.channel.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        



async def setup(bot):
    await bot.add_cog(Channels(bot))
