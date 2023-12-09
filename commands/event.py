import discord
from discord.ext import commands

class event(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self,message:discord.Message):
        if message.author == self.bot.user:
            return
        
        ignored_user_id = 813078218344759326
        if message.author.id == ignored_user_id:
            await message.delete()

        if message.content.startswith("test"):
            await message.channel.send("hello world")
    @commands.Cog.listener()
    async def on_guild_join(self,guild:discord.Guild):
        channel_ = discord.utils.get(self.bot.get_all_channels(), name='console-log-909327_home')
        await channel_.send(f'joined {guild.name}')
        
async def setup(bot):
    await bot.add_cog(event(bot))