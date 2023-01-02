from discord.ext import commands
from util import classes

import discord, os

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
            return await ctx.send(embed=discord.Embed(title="❌ Error", description="Owner only command, fuck off twat"))
        await ctx.send(f"```{error}```")

    

if __name__ == "__main__":
    frost = Frost()
    frost.run()