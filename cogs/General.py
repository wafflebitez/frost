from discord.ext import commands
import discord

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(embed=discord.Embed(title="Pong!", description=f"Client latency: `{round(self.bot.latency * 1000)}ms`"))

    @commands.command()
    async def prefix(self, ctx, new_prefix=None):
        if not ctx.guild:
            if not ctx.author.id == self.bot.config.owner_id:
                return await ctx.send(embed=discord.Embed(title="⚙️ Prefix", description=f"The global prefix is: `{self.bot.config.prefix}`"))
            if not new_prefix:
                return await ctx.send(embed=discord.Embed(title="⚙️ Prefix", description=f"The global prefix is: `{self.bot.config.prefix}`"))
            else:
                self.bot.config.set_prefix(new_prefix)
                return await ctx.send(embed=discord.Embed(title="⚙️ Prefix", description=f"The global prefix has been updated to `{new_prefix}`", color=0x00FF00))
        if not self.bot.servers[ctx.guild.id].is_mod(ctx.author) or new_prefix is None:
            return await ctx.send(embed=discord.Embed(title="⚙️ Prefix", description=f"The prefix for this server is: `{self.bot.servers[ctx.guild.id].prefix}`"))
        self.bot.servers[ctx.guild.id].set_prefix(new_prefix)
        await ctx.send(embed=discord.Embed(title="⚙️ Prefix", description=f"The prefix for this server has been updated to `{new_prefix}`", color=0x00FF00))

    @commands.command()
    @commands.is_owner()
    async def status(self, ctx, *, new_status = "the dumbass didnt provide a status LOL"):
        await self.bot.update_status(new_status)
        response = discord.Embed(title="⚙️ Status", description=f"The bot status has been updated to `{new_status}`", color=0x00FF00)
        await ctx.send(embed=response)

    @commands.command()
    @commands.guild_only()
    async def addmod(self, ctx, role: discord.Role = None):
        if not self.bot.servers[ctx.guild.id].is_mod(ctx.author):
            return await ctx.send(embed=discord.Embed(title="❌ Error", description="You do not have permission to use this command", color=0xFF0000))
        if role is None:
            return await ctx.send(embed=discord.Embed(title="❌ Error", description="You must specify a role to add to the mod list! Try pinging the role or providing the role ID.", color=0xFF0000))
        if self.bot.servers[ctx.guild.id].add_mod(role.id):
            return await ctx.send(embed=discord.Embed(title="✅ Success", description=f"Successfully added **{role.name}** to the list of server mods.", color=0x00FF00))
        else:
            return await ctx.send(embed=discord.Embed(title="❌ Error", description=f"**{role.name}** is already a server mod.", color=0xFF0000))

    @commands.command()
    @commands.guild_only()
    async def removemod(self, ctx, role: discord.Role = None):
        if not self.bot.servers[ctx.guild.id].is_mod(ctx.author):
            return await ctx.send(embed=discord.Embed(title="❌ Error", description="You do not have permission to use this command", color=0xFF0000))
        if role is None:
            return await ctx.send(embed=discord.Embed(title="❌ Error", description="You must specify a role to remove from the mod list! Try pinging the role or providing the role ID.", color=0xFF0000))
        if self.bot.servers[ctx.guild.id].remove_mod(role.id):
            return await ctx.send(embed=discord.Embed(title="✅ Success", description=f"Successfully removed **{role.name}** from the list of server mods.", color=0x00FF00))
        else:
            return await ctx.send(embed=discord.Embed(title="❌ Error", description=f"**{role.name}** is not a server mod.", color=0xFF0000))

    @commands.command()
    @commands.guild_only()
    async def modlist(self, ctx):
        if not self.bot.servers[ctx.guild.id].is_mod(ctx.author):
            return await ctx.send(embed=discord.Embed(title="❌ Error", description="You do not have permission to use this command", color=0xFF0000))
        mod_list = self.bot.servers[ctx.guild.id].moderators
        if len(mod_list) == 0:
            return await ctx.send(embed=discord.Embed(title="❌ Error", description="There are no mods for this server. Use `addmod` to add a mod role.", color=0xFF0000))
        named_list = []
        for role_id in mod_list:
            role = ctx.guild.get_role(role_id)
            if role is None:
                self.bot.servers[ctx.guild.id].remove_mod(role_id)
                continue
            named_list.append(f'**{role.name}**')
        return await ctx.send(embed=discord.Embed(title="🛠️ Mod List", description=", ".join(named_list)), color=0x45B6FE)

        

async def setup(bot):
    await bot.add_cog(General(bot))
