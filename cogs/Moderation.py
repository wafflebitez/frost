from discord.ext import commands

import discord

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Update the bot's prefix or view the current prefix.\n\nUsage: `prefix [new_prefix]`")
    async def prefix(self, ctx, new_prefix=None):
        if not ctx.guild:
            if not ctx.author.id == self.bot.config.owner_id:
                return await ctx.send(embed=discord.Embed(title="Prefix", description=f"The global prefix is: `{self.bot.config.prefix}`", color=0x45B6FE))
            if not new_prefix:
                return await ctx.send(embed=discord.Embed(title="Prefix", description=f"The global prefix is: `{self.bot.config.prefix}`", color=0x45B6FE))
            else:
                self.bot.config.set_prefix(new_prefix)
                return await ctx.send(embed=discord.Embed(title="Prefix", description=f"The global prefix has been updated to `{new_prefix}`", color=0x50C878))
        if not self.bot.servers[ctx.guild.id].is_mod(ctx.author) or new_prefix is None:
            return await ctx.send(embed=discord.Embed(title="Prefix", description=f"The prefix for this server is: `{self.bot.servers[ctx.guild.id].prefix}`", color=0x45B6FE))
        self.bot.servers[ctx.guild.id].set_prefix(new_prefix)
        return await ctx.send(embed=discord.Embed(title="Prefix", description=f"The prefix for this server has been updated to `{new_prefix}`", color=0x50C878))

    @commands.command(help="Add a role to the list of server mods.\n\nUsage: `addmod @role`")
    @commands.guild_only()
    async def addmod(self, ctx, role: discord.Role = None):
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send(embed=discord.Embed(title="Error", description="You do not have permission to use this command", color=0xDC143C))
        if role is None:
            return await ctx.send(embed=discord.Embed(title="Error", description="You must specify a role!", color=0xDC143C))
        if self.bot.servers[ctx.guild.id].add_mod(role.id):
            return await ctx.send(embed=discord.Embed(title="Success", description=f"Successfully added **{role.name}** to the list of server mods.", color=0x50C878))
        else:
            return await ctx.send(embed=discord.Embed(title="Error", description=f"**{role.name}** is already a server mod.", color=0xDC143C))

    @commands.command(aliases=['delmod', 'deletemod'], help="Remove a role from the list of server mods.\n\nUsage: `removemod @role`")
    @commands.guild_only()
    async def removemod(self, ctx, role: discord.Role = None):
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send(embed=discord.Embed(title="Error", description="You do not have permission to use this command", color=0xDC143C))
        if role is None:
            return await ctx.send(embed=discord.Embed(title="Error", description="You must specify a role!", color=0xDC143C))
        if self.bot.servers[ctx.guild.id].remove_mod(role.id):
            return await ctx.send(embed=discord.Embed(title="Success", description=f"Successfully removed **{role.name}** from the list of server mods.", color=0x50C878))
        else:
            return await ctx.send(embed=discord.Embed(title="Error", description=f"**{role.name}** is not a server mod.", color=0xDC143C))

    @commands.command(aliases=['getmods', 'mods'], help="List the server mods.\n\nUsage: `listmods`")
    @commands.guild_only()
    async def listmods(self, ctx):
        if not self.bot.servers[ctx.guild.id].is_mod(ctx.author):
            return await ctx.send(embed=discord.Embed(title="Error", description="You do not have permission to use this command", color=0xDC143C))
        mod_list = self.bot.servers[ctx.guild.id].moderators
        if len(mod_list) == 0:
            return await ctx.send(embed=discord.Embed(title="Error", description="There are no mods for this server. Use `addmod` to add a mod role.", color=0xDC143C))
        named_list = []
        for role_id in mod_list:
            role = ctx.guild.get_role(role_id)
            if role is None:
                self.bot.servers[ctx.guild.id].remove_mod(role_id)
                continue
            named_list.append(f'**{role.name}**')
        return await ctx.send(embed=discord.Embed(title="Mod List", description=", ".join(named_list), color=0x45B6FE))


async def setup(bot):
    await bot.add_cog(Moderation(bot))