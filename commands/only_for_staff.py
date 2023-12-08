import discord
from discord.ext import commands
import requests
from io import BytesIO
class general(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @commands.command(name="check")
    async def _test(self,i:commands.Context,channel):
        """| <check [your channel name] this command is for check if bot is fine with any channel"""
        sent_ = discord.utils.get(self.bot.get_all_channels(), name=channel)
        await sent_.send("hello world")

    @commands.command(name="emoji")
    async def _emoji(self,ctx):
        await ctx.send(":Yoshi:")

    @commands.command(name="pfp")
    async def _pfp(self,i:commands.Context,url):
        """| here only for owner"""
        role = discord.utils.get(i.guild.roles, name='909327_home')
        if role not in i.author.roles:
            await i.send('you do not have permission to use this command')
            return
        respone = requests.get(url)
        image_idk = BytesIO(respone.content)
        await self.bot.user.edit(avatar=image_idk.read())
        await i.send("my pfp has been c<hanged")
    
    @commands.command(name='createrole')
    async def _createrole(self,i:commands.Context,role_name):
        """| here only for owner"""
        role = discord.utils.get(i.guild.roles, name=role_name)
        if role:
            await i.send(f'{role_name} already have')
            return
        new_role = await i.guild.create_role(name=role_name)
        await i.send(f'we have created role {new_role.name}!')
    
    @commands.command(name='addrole')
    async def _addrole(self,i:commands.Context,member:discord.Member,role_name):
        """| here only for owner"""
        old_role = discord.utils.get(i.guild.roles, name=role_name)
        if not old_role:
            await i.send(f'role {role_name} not found bruh')
            return
        
        await member.add_roles(old_role)
        await i.send(f'we add {member.name} in role {old_role} ggs!')
    
    async def new_name(self,newname):
        await self.bot.user.edit(username=newname)

    @commands.command(name='change_name')
    async def _change_name(self,i:commands.Context,*,new):
        """| here only for owner"""
        role = discord.utils.get(i.guild.roles,name='909327_home')
        if not role:
            await i.send("you can't use this command")
            return
        else:
            await self.new_name(newname=new)
            await i.send("my name has been changed")

    @commands.command(name='bot_guild')
    async def _guild(self,i:commands.Context):
        role = discord.utils.get(i.guild.roles,name='909327_home')
        if not role:
            await i.send("you can't use this command")
            return
        else:
            guild_names = '\n'.join(guild.name for guild in self.bot.guilds)
            await i.send(f'\n{guild_names}')

async def setup(bot):
    await bot.add_cog(general(bot))