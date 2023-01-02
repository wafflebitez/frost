from discord.ext import commands
from util import classes

import discord, os



class Help(commands.HelpCommand):

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", description="Currently, the following commands are available:", color=0x45B6FE)
        for cog in mapping:
            if cog:
                embed.add_field(name=cog.qualified_name, value=" ".join([f"`{self.context.prefix}{c.name}`" for c in mapping[cog]]), inline=False)
        embed.set_footer(text="Use 'help [command]' for more info on a command.")
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=f"Help: {command.name}", description=command.help, color=0x45B6FE)
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(title=f"Help: {cog.qualified_name}", description=cog.description, color=0x45B6FE)
        for command in cog.get_commands():
            embed.add_field(name=command.name, value=command.help, inline=False)
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=f"Help: {group.name}", description=group.help, color=0x45B6FE)
        for command in group.commands:
            embed.add_field(name=command.name, value=command.help, inline=False)
        await self.get_destination().send(embed=embed)



class Frost(commands.Bot):

    async def get_prefix(self, message):
        if message.guild is None:
            return self.config.prefix
        else:
            if message.guild.id not in self.servers:
                self.servers[message.guild.id] = classes.Server(self, message.guild.id)
            return self.servers[message.guild.id].prefix

    def __init__(self):
        self.config = classes.Config()
        self.servers = {}
        super().__init__(command_prefix=self.get_prefix, case_insensitive=True, intents=discord.Intents.all(), owner_id=self.config.owner_id)
        self.help_command = Help()
        
    async def on_ready(self):
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                await self.load_extension(f"cogs.{file[:-3]}")
                print(f"[INFO] Loaded extension: {file[:-3]}")
        print(f"[INFO] Logged in as {self.user.name}#{self.user.discriminator}")
        await self.change_presence(activity=discord.Game(self.config.status))
        print(f"[INFO] Status set to: {self.config.status}")

    async def update_status(self, status):
        self.config.set_status(status)
        await self.change_presence(activity=discord.Game(status))

    def run(self):
        super().run(self.config.token, reconnect=True)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.NotOwner):
            return await ctx.send(embed=discord.Embed(title="Error", description="This command is restricted to only the bot owner.", color=0xDC143C))
        await ctx.send(f"```{error}```")



if __name__ == "__main__":
    frost = Frost()
    frost.run()