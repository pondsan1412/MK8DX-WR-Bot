import discord
from discord.ext import commands
from discord.ui import Select, View, Button
from discord import Embed
from datetime import datetime
# Class for select button
class HelpSelect(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(
            label="World Records Table Command", 
            emoji='<a:yellow_earth:1182224911813582858>', 
            description="World Record Info 150cc & 200cc"),
            discord.SelectOption(
                label="General Command List",
                emoji='<:x_mark98:1182224905677324368>',
                description='Just normal command list'
            ),
            discord.SelectOption(
                label="Main Page",
                emoji='<:Rip:1182226264011046963>',
                description="Just go back to main page"
            ),
            discord.SelectOption(
                label="Abbreviations  Page [Standard Track]",
                emoji='<a:book93:1182224907980001320>',
                description='Track\'s abbreviations list: S track'
            ),
            discord.SelectOption(
                label='Abbreviations  Track [DLC Track]',
                emoji='<a:book93:1182224907980001320>',
                description='Track\'s abbreviations list: DLC track'
            )
        ]
        
        super().__init__(
            placeholder="📝 Command Category List",
            max_values=1,
            min_values=1,
            options=options
        )
        

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "World Records Table Command":
            embed_table = Embed(title='Table Stuff Commands',color=discord.Color.orange(),type="rich")
            embed_table.add_field(
                name="Command List",
                value=
"""
**__wr:__** displaying world record of currently anytrack example `?wr rMC` \n

**__Explaining__**
`wr` command can displaying both of 150cc and 200cc table just press between those button and you must have patience\n
it may cause a few time to search infomation
if you don't know the abbreviations  of track just find in select option [Abbreviations  Page] in help command\n
we will do emoji instead of track name soon.
"""
            )
            embed_table.set_author(name=interaction.user.name,url=interaction.user.display_avatar,icon_url=interaction.user.display_avatar)
            await interaction.response.edit_message(embed=embed_table)
        if self.values[0] == "General Command List":
            embed_general = Embed(title='General Command List',color=discord.Color.green())
            embed_general.add_field(
                name="in progressing",
                value=
"""** In processing.... not yet for now"""
            )
            embed_general.set_author(name=interaction.user.name,icon_url=interaction.user.display_avatar)
            await interaction.response.edit_message(embed=embed_general)
        if self.values[0] =="Main Page":
            
            embedSelect = discord.Embed(
            color=discord.Color.purple(),
            title="A Help Commands",
            description=
            """
Prefix is: **?**
""",
        )
            embedSelect.add_field(name="Support Stuff",value='[Official WR MK8DX\'s website](https://pondsan1412.github.io/MK8DX-WR-Bot/)\n[visit our support server](https://discord.gg/JMeaVU7W)')
            embedSelect.add_field(name='Developer Team ',value='\n <@324207503816654859> \n <@257332011075764224>',inline=False)
            embedSelect.set_image(url="https://cdn.discordapp.com/attachments/1176922445941313617/1181838263313498122/Rip.png?ex=658283a7&is=65700ea7&hm=6b17082d0153d9180b52f35c0a3a35732a70204f18b4db25bc55668639d704a8&")
            embedSelect.set_author(name=interaction.user.name,icon_url=interaction.user.display_avatar)
            await interaction.response.edit_message(embed=embedSelect)
        if self.values[0]== "Abbreviations  Page [Standard Track]":
            embed_abrra = Embed(title='Track\'s Abbreviations  S List',color=discord.Color.greyple())
            embed_abrra.add_field(
                name="S List:",
                value=
                """
Acronym	  Full Name
MKS	  Mario Kart Stadium
WP	  Water Park
SSC	  Sweet Sweet Canyon
TR	  Thwomp Ruins
MC	  Mario Circuit
TH	  Toad Harbor
TM	  Twisted Mansion
SGF	  Shy Guy Falls
SA	  Sunshine Airport
DS	  Dolphin Shoals
Ed	  Electrodrome
MW	  Mount Wario
CC	  Cloudtop Cruise
BDD	  Bone-Dry Dunes
BC	  Bowser's Castle
RR    Rainbow Road
rMMM  Moo Moo Meadows
rMC	  Mario Circuit
rCCB  Cheep Cheep Beach
rTT	  Toad's Turnpike
rDDD  Dry Dry Desert
rDP3  Donut Plains 3
rRRy  Royal Raceway
rDKJ  DK Jungle
rWS	  Wario Stadium
rSL	  Sherbet Land
rMP	  Music Park
rYV	  Yoshi Valley
rTTC  Tick-Tock Clock
rPPS  Piranha Plant Slide
rGV	  Grumble Volcano
rRRd  N64 Rainbow Road
dYC	  Yoshi Circuit
dEA	  Excitebike Arena
dDD	  Dragon Driftway
dMC	  Mute City
dWGM  Wario's Gold Mine
dRR	  SNES Rainbow Road
dIIO  Ice Ice Outpost
dHC	  Hyrule Circuit
dBP	  Baby Park
dCL	  Cheese Land
dWW   Wild Woods
dAC   Animal Crossing
dNBC  Neo Bowser City
dRiR  GBA Ribbon Road
dSBS  Super Bell Subway
dBB   Big Blue
"""
            )
            await interaction.response.edit_message(embed=embed_abrra)
        if self.values[0] =="Abbreviations  Track [DLC Track]":
            embed_abrra_dlc = Embed(title='Track\'s Abbreviations  DLC List')
            embed_abrra_dlc.add_field(
                name='DLC List:',
                value="""
bPP   Paris Promenade
bTC   Toad Circuit
bCMo  Choco Mountain
bCMa  Coconut Mall
bTB   Tokyo Blur
bSR   Shroom Ridge
bSG   Sky Garden
bNH   Ninja Hideaway
bNYM  New York Minute
bMC3  Mario Circuit 3
bKD   Kalimari Desert
bWP   Waluigi Pinball
bSS   Sydney Sprint
bSL   Snow Land
bMG   Mushroom Gorge
bSHS  Sky-High Sundae
bLL   London Loop
bBL   Boo Lake
bRRM  Rock Rock Mountain
bMT   Maple Treeway
bBB   Berlin Byways
bPG   Peach Gardens
bMM   Merry Mountain
bRR7  Rainbow Road
bAD   Amsterdam Drift
bRP   Riverside Park
bDKS  DK Summit
bYI   Yoshi's Island
bBR   Bangkok Rushh
bMC   Mario Circuit
bWS   Waluigi Stadium
bSSy  Singapore Speedway
bAtD  Athens Dash
bDC   Daisy Cruiser
bMH   Moonview Highway
bSCS  Squeaky Clean Sprint
bLAL  Los Angeles Laps
bSW   Sunset Wilds
bKC   Koopa Cape
bVV   Vancouver Velocity
bRA   Rome Avanti
bDKM  DK Mountain
bDCt  Daisy Circuit
bPPC  Piranha Plant Cove
bMD   Madrid Drive
bRIW  Rosalina's Ice World
bBC3  Bowser Castle 3
bRRw  Rainbow Road
"""
            )
            
            await interaction.response.edit_message(embed=embed_abrra_dlc)
            

# Class for the view
class HelpSelectView(discord.ui.View):
    def __init__(self, *, timeout=120):
        super().__init__(timeout=timeout)
        self.add_item(HelpSelect())



class Help(commands.Cog):
    """Help commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def console_log(self,ctx: commands.Context, channelstr,parameter):
        console_ = discord.utils.get(self.bot.get_all_channels(), name=channelstr)
        embed = Embed(title=f"Command usage: {ctx.command.name}",color=discord.Color.blurple())
        embed.set_author(name=ctx.author.name,icon_url=ctx.author.display_avatar)
        embed.add_field(name=f'channel: {ctx.channel}',value=f'**___time___**: `{datetime.now()}`\n **___parameter values___**: `{parameter}`')
        embed.set_footer(text=f'author server: {ctx.guild.name}')
        embed.set_thumbnail(url=ctx.guild.icon)
        
        await console_.send(embed=embed)
        return console_
    
    @commands.hybrid_command(name="help")
    async def _selectmenus(self, ctx: commands.Context):
        """A help command"""
        await self.console_log(ctx, "console-log-909327_home",None)
        embedSelect = discord.Embed(
            color=discord.Color.purple(),
            title="A Help Commands",
            description=
            """
Prefix is: **?**
or you can mention bot like `@botname wr rMC`
""",
        )
        embedSelect.add_field(name="Support Stuff",value='[bot\'s official website](https://pondsan1412.github.io/MK8DX-WR-Bot/)\n**report bugs, problem**\n[visit our support server](https://discord.gg/JMeaVU7W)')
        embedSelect.add_field(name='Developer Team ',value='\n <@324207503816654859> founder/developer \n <@257332011075764224> tester/helper',inline=False)
        embedSelect.set_image(url="https://cdn.discordapp.com/attachments/1176922445941313617/1181838263313498122/Rip.png?ex=658283a7&is=65700ea7&hm=6b17082d0153d9180b52f35c0a3a35732a70204f18b4db25bc55668639d704a8&")
        embedSelect.set_author(name=ctx.author.name,icon_url=ctx.author.display_avatar)
        return_back = HelpSelect()
        await ctx.send(embed=embedSelect, view=HelpSelectView())

async def setup(bot):
    await bot.add_cog(Help(bot))
