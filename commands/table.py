import re
from PIL import Image
import requests
from io import BytesIO
import aiohttp
import discord
from bs4 import BeautifulSoup
from discord import Embed
from discord.ext import commands
from mk8dx import Track
from pytube import YouTube
import asyncio
from function import player_mii_pfp
import function
from datetime import datetime
from fuzzywuzzy import fuzz
class MyView(discord.ui.View):
    def __init__(
            self,
            url,
            message,
            trackname,
            embed,
            url200cc,
            url150cc
            
    ):
        super().__init__(timeout=3600)
        self.url = url
        button = discord.ui.Button(label=' ', style=discord.ButtonStyle.url, url=f'{self.url or "https://www.the-video-has-not-been-verified-yet.com"}', emoji="<a:youtube_gif:1181809823898153020")
        self.add_item(button)
        self.message = message
        self.trackname = trackname
        self.embed = embed
        self.after_freeze = None
        self.switch = True
        self.url200cc = url200cc
        self.url150cc = url150cc
    
    @discord.ui.button(
            label="watch in discord",
            style=discord.ButtonStyle.blurple,
            emoji="<a:srt_discordloading:1175832338597429358>",
            disabled=False
    )
    async def youtube_discord(self, interaction:discord.Interaction,button:discord.ui.Button):
            
            if self.url:
                await interaction.response.send_message(f"{self.url}",delete_after=120)
            else:
                await interaction.response.send_message("The video is not verified yet \n please click the button to watch previous world record video instead",delete_after=10)
                def convert_html_track(track):
                    result = Track.from_nick(f'{track}').full_name.replace(' ', '+')
                    return result
                
                def find_minimum_time_url(url):
                    response = requests.get(url)
                    html_code = response.content
                    soup = BeautifulSoup(html_code, 'html.parser')
                    all_rows = soup.select('.wr tr')
                    min_time_url = None
                    for row in all_rows:
                        youtube_url_td = row.select_one('td a[href^="https://www.youtube.com/watch"]')
                        if youtube_url_td:
                            time_td = row.select_one('td:nth-of-type(2)')
                            time = time_td.text.strip()
                            if min_time_url is None or time < min_time_url['time']:
                                min_time_url = {'time': time, 'url': youtube_url_td['href']}
                    return min_time_url
                
                def url_found(url_to_check):
                    url_to_check_ = url_to_check
                    result = find_minimum_time_url(url_to_check_)
                    if result:
                        return (f"{result['url']}")
                    else:
                        return("No data found.")
                convert_track_html = convert_html_track(track=f'{self.trackname}')
                check = url_found(url_to_check=f"https://mkwrs.com/mk8dx/display.php?track={convert_track_html}&m=200")
                if self.url200cc is None:
                    self.add_item(
                        discord.ui.Button(
                            label='watch previous wr video',
                            style=discord.ButtonStyle.url,
                            url=f'{check}'

                        )
                    )
                if self.url150cc is None:
                    convert_track_html = convert_html_track(track=f'{self.trackname}')
                    check = url_found(url_to_check=f"https://mkwrs.com/mk8dx/display.php?track={convert_track_html}")
                    self.add_item(
                        discord.ui.Button(
                            label='watch previous wr video',
                            style=discord.ButtonStyle.url,
                            url=f'{check}'

                        )
                    )
            message_ = interaction.message
            shiny_button = None
            for child in self.children:
                if type(child) == discord.ui.Button and child.label == "watch in discord":
                    shiny_button = child
                    child.disabled = True
                    break
            await interaction.message.edit(view=self)
            await asyncio.sleep(119)
            shiny_button.disabled = False
            await interaction.message.edit(view=self)

    @discord.ui.button(label="200cc",style=discord.ButtonStyle.red,disabled=False,custom_id="e308f")
    async def swapCC(self,interaction:discord.Interaction,button:discord.ui.Button):
        await interaction.response.defer()

        global old_link
        message = self.message
        message_edit = message
        abbra_track = self.trackname
        old_linkyoutube = self.url

        

        abbra_emoji_old = abbra_track
        def compare_track(abbra):
            try:
                list_track = Track.from_nick(nick=abbra).full_name
                track_name = list_track
                return track_name
            except AttributeError:
                return f'{abbra} is not in the tracks list'

        result = compare_track(abbra=abbra_track)

        #here full function for video link
        async def get_track_url(trackname, url):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    html_content = await response.text()

            soup = BeautifulSoup(html_content, 'html.parser')
            wr_table = soup.find('table', class_='wr')

            try:
                if wr_table:
                    for row in wr_table.find_all('tr')[1:]:
                        columns = row.find_all('td')
                        track = columns[0].a.text.strip()
                        date_ = columns[4].text.strip()
                        player_ = columns[2].text.strip()
                        img_tag = columns[3].center.img
                        nation_ = img_tag['title'] if img_tag else None
                        src_value = img_tag['src']
                        combo_charecter = columns[6].text.strip()
                        combo_vehicle = columns[7].text.strip()
                        combo_roller = columns[8].text.strip()
                        combo_glider = columns[9].text.strip()
                        # Provide a default value if columns[10] is None
                        duration_ = columns[5].text.strip()
                        full_url = f'https://mkwrs.com/mk8dx/{src_value}'
                        onmouseover_attr = columns[10].img.get('onmouseover', '')
                        splits_values = [value.strip() for value in onmouseover_attr[15:-2].split("', '")]
                        re.search(r"show_splits\('([^']+)', '([^']+)', '([^']+)', '([^']+)', '([^']+)'", onmouseover_attr)
                        player_profile = columns[2].a['href']

                        # Check if columns[1].a is not None before accessing its text attribute
                        time_ = columns[1].a.text.strip() if columns[1].a else columns[1].text.strip()

                        if splits_values:
                            lap1, lap2, lap3, coins, shroom = splits_values[1:6]
                        else:
                            lap1, lap2, lap3, coins, shroom = '', '', '', '', ''


                        if track.lower() == trackname.lower():
                            return (
                                columns[1].a['href'] if columns[1].a else None,

                                date_,
                                player_,
                                nation_,
                                full_url,
                                time_,
                                combo_charecter,
                                combo_vehicle,
                                combo_glider,
                                combo_roller,
                                duration_,
                                lap1,
                                lap2,
                                lap3,
                                coins,
                                shroom,
                                player_profile
                            )


                    # Track not found
                    return None
                else:
                    # No World Records table found
                    return None
            except TypeError as e:
                pass

            except AttributeError as e:
                # Print relevant information for debugging
                print(f"AttributeError: {e} ")

                return f"Error: AttributeError in get_track_url for track {trackname} \n {player_}\n   \n {e}"



        url = "https://mkwrs.com/mk8dx/wrs_200.php?date=0"

        trackname = result
        if trackname == "SNES Bowser's Castle 3":
            trackname = "SNES Bowser Castle 3"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                await response.text()

        result = await get_track_url(trackname, url)
        
        def is_thumbnail_size(url):
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            return image.size == (120, 90)
        
        def youtube_id(url):
            try:
                video = YouTube(url)
                video_id = video.video_id
                return video_id 
            except Exception as e:
                return None
            
        #convert link for thumbnail youtube
        def convert_thumnail(link):    
            if is_thumbnail_size(link):
                thumbnail_url_new = f"http://i3.ytimg.com/vi/{video_id}/hqdefault.jpg"
            else:
                thumbnail_url_new = link
            return thumbnail_url_new
        

        if isinstance(result, tuple):
            # Unpack tuple values
            track_url, date_, player_, nation_, full_url, time_, combo_charecter, combo_vegicle, combo_glider, combo_roller, duration_, lap1, lap2, lap3, coins, shroom, player_profile = result
            #here check player's name return their picture picture profile 
            mii_pfp = player_mii_pfp(player_name=player_)
            # Get video information
            video_picture_url = track_url
            video_id = youtube_id(video_picture_url)
            thumbnail_url = f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg'
            convert_thumnail_ = convert_thumnail(link=thumbnail_url)
            # Format player name
            player_ = f"{player_}"
            name_parts = player_.split(" ")
            " ".join(name_parts[:-1]).rstrip()

            #convert emoji for combination
            def find_emoji(input_str, emoji_list):
                # สร้างตัวแปรเพื่อเก็บ emoji ที่เจอ
                found_emoji = None
                
                # วนลูปตามทุกรูปแบบของ emoji ใน list
                for emoji in sorted(emoji_list, key=len, reverse=True):
                    # เอาเฉพาะตัวอักษรภาษาอังกฤษใน emoji
                    emoji_chars = [char for char in emoji if char.isalpha()]
                    emoji_str = ''.join(emoji_chars)
                    
                    # ถ้า input_str มี substring ของ emoji_str (โดยต้องตรวจสอบว่าทุกตัวอักษรภาษาอังกฤษใน emoji_str ต้องอยู่ใน input_str)
                    if all(char.lower() in input_str.lower() for char in emoji_str):
                        found_emoji = emoji
                        break
                
                # คืนค่า emoji ที่เจอ (หากมี) หรือ None (หากไม่เจอ)
                return found_emoji
            
            if abbra_emoji_old == 'bdct':
                abbra_emoji_old = 'bdci'

            def convert_emoji(emoji_name):
                abbr_ = Track.from_nick(f'{emoji_name}').abbr
                result = f"{abbr_}"
                return result
            
            result_emoji = convert_emoji(emoji_name=abbra_emoji_old)
            
            print(result_emoji)

            if result_emoji == 'bDCi':
                result_emoji = 'daisycircuit'

            def find_emoji(input_str, emoji_list):
                # สร้างตัวแปรเพื่อเก็บ emoji ที่เจอ
                found_emoji = None
                highest_ratio = 0  # ตัวแปรเพื่อเก็บค่าความเหมือนสูงสุด
                
                # แปลง input_str ให้เป็นตัวพิมพ์เล็กทั้งหมด
                input_str = input_str.lower()
                
                # วนลูปตามลำดับของ emoji ใน list
                for emoji in emoji_list:
                    # แปลง emoji ให้เป็นตัวพิมพ์เล็กทั้งหมด
                    emoji_lower = emoji.lower()
                    
                    # เอาเฉพาะตัวอักษรภาษาอังกฤษใน emoji
                    emoji_chars = [char for char in emoji_lower if char.isalpha()]
                    emoji_str = ''.join(emoji_chars)
                    
                    # คำนวณค่าความเหมือนระหว่าง input_str กับ emoji_str
                    ratio = fuzz.ratio(input_str, emoji_str)
                    
                    # ถ้า ratio มีค่ามากกว่าค่าความเหมือนสูงสุดที่เคยพบ
                    if ratio > highest_ratio:
                        highest_ratio = ratio
                        found_emoji = emoji
                
                return found_emoji
            
            emoji_list = function.standard_emoji_track
            emoji_track_ = find_emoji(input_str=result_emoji, emoji_list=emoji_list)
            #charecter list
            list_character = combo_charecter
            result = find_emoji(list_character, function.character_list_emoji)
            emoji_character = result
            #kart list
            list_kart = combo_vegicle
            function_kart = find_emoji(list_kart, function.kart_list_emoji)
            emoji_kart = function_kart
            #tires list
            list_tires = combo_roller
            function_tires = find_emoji(list_tires, function.tires_list_emoji)
            emoji_tires = function_tires
            #glider list
            list_glider = combo_glider
            function_glider = find_emoji(list_glider, function.glider_list_emoji)
            emoji_glider = function_glider

            # Create Discord Embed
            embed = Embed(colour=15548997,title=f'**World Record __200cc__**  \n**___{trackname}___** {emoji_track_} ')
            embed.set_thumbnail(url=mii_pfp)
            embed.set_author(name=f"{player_}'s profile", icon_url=f"{full_url}", url=f"https://mkwrs.com/mk8dx/{player_profile}")
            embed.add_field(
                name=f" ",
                value = f"""
                    Verified Date: **{date_}**
**___Time:___** ```ini
[{time_}]
```
WR HOLDER: **{player_}**
Country: **{nation_}**
Length Day: **{duration_}**
**__lap time__** :stopwatch:
:one: {lap1}
:two: {lap2}
:three: {lap3}
<:threemushrooms:1175155099971096679> **{shroom}**
<:item000Coin:1175154443306668192> **{coins}**

**___Combination___**
charecter: **{combo_charecter}** {emoji_character}
vehicle: **{combo_vegicle} {emoji_kart}**
roller: **{combo_roller}  {emoji_tires}**
glider: **{combo_glider} {emoji_glider}**
                """)
            if video_id is not None:
                embed.set_image(url=f"{convert_thumnail_}")
            else:
                new_thumbnail = f"https://cdn.discordapp.com/attachments/1172493621732327495/1182027246630866944/image.png?ex=658333a8&is=6570bea8&hm=b4eba452c2b85bd8d744c577725402dcea4a9cedd3813d56a057deba5bb1c3ee&"
                embed.set_image(url=f"{new_thumbnail}")
            
            embed.set_footer(text="")
            if track_url is None:
                embed.set_footer(text="**___The video is not verified yet but you can watch previous wr video**")
                new_embed = embed
                return_200cc = MyView(url=track_url, message=message_edit,trackname=abbra_track,embed=self.embed,url200cc=track_url,url150cc=" ")
                await message_edit.edit(embed=new_embed)
            else:
                
                 # ส่ง Embed กลับในแชท
                try:
                    old_embed = self.embed
                    new_url = track_url
                    after_freeze = MyView(url=new_url, message=message_edit,trackname=abbra_track,embed=old_embed,url200cc=track_url,url150cc=" ")
                    self.after_freeze = after_freeze
                    await message_edit.edit(embed=embed, view=self.after_freeze)
                    
                except:
                    pass
        else:
            await message_edit.edit(result)
        old_embed_ = self.embed
        new_url_ = track_url
        after_freeze_=MyView(url=new_url_, message=message_edit,trackname=abbra_track,embed=old_embed_,url200cc=track_url,url150cc=" ")
        await message.edit(embed=embed)
        message_ = interaction.message
        shiny_button = None
        for child in after_freeze_.children:
            if type(child) == discord.ui.Button and child.label == "200cc":
                shiny_button = child
                child.disabled = True
                break
        self.switch = False
        
        await interaction.message.edit(view=after_freeze_)
        old_link = MyView(url=old_linkyoutube, message=message_edit,trackname=abbra_track,embed=self.embed,url200cc=track_url,url150cc=" ")

    global old_link    
    @discord.ui.button(label="150cc",style=discord.ButtonStyle.green,disabled=False)
    async def _150cc(self,interaction:discord.Interaction,button:discord.ui.Button):
        
        global old_link
        await interaction.response.defer()
        message_ = interaction.message
        shiny_button = None
        for child in self.children:
            if type(child) == discord.ui.Button and child.label == "150cc":
                shiny_button = child
                child.disabled = True
                break
        
        
        await interaction.message.edit(embed=self.embed,view=old_link)
            
        



class mk8dxwr(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
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
    
    @commands.hybrid_command(name='wr')
    async def worldrecord(self,ctx:commands.Context, abbra_track):
        """display world record of anytrack for currently track from mk8dxwr.com"""
        await ctx.defer()
        await self.console_log(ctx, "console-log-909327_home",abbra_track)
        
        if abbra_track.lower() == 'bdct':
            abbra_track = 'bdci'

        abbra_emoji_old = abbra_track

        def compare_track(abbra):
            try:
                list_track = Track.from_nick(nick=abbra).full_name
                track_name = list_track
                return track_name
            except AttributeError:
                return f'{abbra} is not in the tracks list'

        result = compare_track(abbra=abbra_track)
    
        #here full function for video link
        async def get_track_url(trackname, url):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    html_content = await response.text()

            soup = BeautifulSoup(html_content, 'html.parser')
            wr_table = soup.find('table', class_='wr')

            try:
                if wr_table:
                    for row in wr_table.find_all('tr')[1:]:
                        columns = row.find_all('td')
                        track = columns[0].a.text.strip()
                        date_ = columns[4].text.strip()
                        player_ = columns[2].text.strip()
                        img_tag = columns[3].center.img
                        nation_ = img_tag['title'] if img_tag else None
                        src_value = img_tag['src']
                        combo_charecter = columns[6].text.strip()
                        combo_vehicle = columns[7].text.strip()
                        combo_roller = columns[8].text.strip()
                        combo_glider = columns[9].text.strip()
                        # Provide a default value if columns[10] is None
                        duration_ = columns[5].text.strip()
                        full_url = f'https://mkwrs.com/mk8dx/{src_value}'
                        onmouseover_attr = columns[10].img.get('onmouseover', '')
                        splits_values = [value.strip() for value in onmouseover_attr[15:-2].split("', '")]
                        re.search(r"show_splits\('([^']+)', '([^']+)', '([^']+)', '([^']+)', '([^']+)'", onmouseover_attr)
                        player_profile = columns[2].a['href']

                        # Check if columns[1].a is not None before accessing its text attribute
                        time_ = columns[1].a.text.strip() if columns[1].a else columns[1].text.strip()

                        if splits_values:
                            lap1, lap2, lap3, coins, shroom = splits_values[1:6]
                        else:
                            lap1, lap2, lap3, coins, shroom = '', '', '', '', ''


                        if track.lower() == trackname.lower():
                            return (
                                columns[1].a['href'] if columns[1].a else None,

                                date_,
                                player_,
                                nation_,
                                full_url,
                                time_,
                                combo_charecter,
                                combo_vehicle,
                                combo_glider,
                                combo_roller,
                                duration_,
                                lap1,
                                lap2,
                                lap3,
                                coins,
                                shroom,
                                player_profile
                            )


                    # Track not found
                    return None
                else:
                    # No World Records table found
                    return None
            except TypeError as e:
                pass

            except AttributeError as e:
                # Print relevant information for debugging
                print(f"AttributeError: {e} ")

                return f"Error: AttributeError in get_track_url for track {trackname} \n {player_}\n   \n {e}"



        url = "https://mkwrs.com/mk8dx/wrs.php?date=0"

        trackname = result
        if trackname == "SNES Bowser's Castle 3":
            trackname = "SNES Bowser Castle 3"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                await response.text()

        result = await get_track_url(trackname, url)

        def youtube_id(url):
            try:
                video = YouTube(url)
                video_id = video.video_id
                return video_id 
            except Exception as e:
                return None

        if isinstance(result, tuple):
            # Unpack tuple values
            track_url, date_, player_, nation_, full_url, time_, combo_charecter, combo_vegicle, combo_glider, combo_roller, duration_, lap1, lap2, lap3, coins, shroom, player_profile = result
            #here check player's name return their picture picture profile 
            print(player_)
            mii_pfp = player_mii_pfp(player_name=player_)
            # Get video information
            video_picture_url = track_url
            video_id = youtube_id(video_picture_url)
            thumbnail_url = f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg'

            # Format player name
            player_ = f"{player_}"
            name_parts = player_.split(" ")
            " ".join(name_parts[:-1]).rstrip()

            def find_emoji(input_str, emoji_list):
                # สร้างตัวแปรเพื่อเก็บ emoji ที่เจอ
                found_emoji = None
                
                # วนลูปตามทุกรูปแบบของ emoji ใน list
                for emoji in sorted(emoji_list, key=len, reverse=True):
                    # เอาเฉพาะตัวอักษรภาษาอังกฤษใน emoji
                    emoji_chars = [char for char in emoji if char.isalpha()]
                    emoji_str = ''.join(emoji_chars)
                    
                    # ถ้า input_str มี substring ของ emoji_str (โดยต้องตรวจสอบว่าทุกตัวอักษรภาษาอังกฤษใน emoji_str ต้องอยู่ใน input_str)
                    if all(char.lower() in input_str.lower() for char in emoji_str):
                        found_emoji = emoji
                        break
    
    # คืนค่า emoji ที่เจอ (หากมี) หรือ None (หากไม่เจอ)
                return found_emoji


            #charecter list
            list_character = combo_charecter
            result = find_emoji(list_character, function.character_list_emoji)
            emoji_character = result
            #kart list
            list_kart = combo_vegicle
            function_kart = find_emoji(list_kart, function.kart_list_emoji)
            emoji_kart = function_kart
            #tires list
            list_tires = combo_roller
            function_tires = find_emoji(list_tires, function.tires_list_emoji)
            emoji_tires = function_tires
            #glider list
            list_glider = combo_glider
            function_glider = find_emoji(list_glider, function.glider_list_emoji)
            emoji_glider = function_glider

            def convert_emoji(emoji_name):
                abbr_ = Track.from_nick(f'{emoji_name}').abbr
                result = f"{abbr_}"
                return result
            
            result_emoji = convert_emoji(emoji_name=abbra_emoji_old)
            print(result_emoji)

            #swap abbravations for fixing problems
            if result_emoji == 'bDCi':
                result_emoji = 'daisycircuit'

            def find_emoji(input_str, emoji_list):
                # สร้างตัวแปรเพื่อเก็บ emoji ที่เจอ
                found_emoji = None
                highest_ratio = 0  # ตัวแปรเพื่อเก็บค่าความเหมือนสูงสุด
                
                # แปลง input_str ให้เป็นตัวพิมพ์เล็กทั้งหมด
                input_str = input_str.lower()
                
                # วนลูปตามลำดับของ emoji ใน list
                for emoji in emoji_list:
                    # แปลง emoji ให้เป็นตัวพิมพ์เล็กทั้งหมด
                    emoji_lower = emoji.lower()
                    
                    # เอาเฉพาะตัวอักษรภาษาอังกฤษใน emoji
                    emoji_chars = [char for char in emoji_lower if char.isalpha()]
                    emoji_str = ''.join(emoji_chars)
                    
                    # คำนวณค่าความเหมือนระหว่าง input_str กับ emoji_str
                    ratio = fuzz.ratio(input_str, emoji_str)
                    
                    # ถ้า ratio มีค่ามากกว่าค่าความเหมือนสูงสุดที่เคยพบ
                    if ratio > highest_ratio:
                        highest_ratio = ratio
                        found_emoji = emoji
                
                return found_emoji
            
            emoji_list = function.standard_emoji_track
            emoji_track_ = find_emoji(input_str=result_emoji, emoji_list=emoji_list)
            # Create Discord Embed
            embed = Embed(colour=3447003,title=f'**World Record __150cc__** \n**___{trackname}___** {emoji_track_} ')
            embed.set_thumbnail(url=mii_pfp)
            embed.set_author(name=f"{player_}'s profile", icon_url=f"{full_url}", url=f"https://mkwrs.com/mk8dx/{player_profile}")

#dont move embed field (and add anything you want but dont move line or row)
            embed.add_field(
                name=f"",
                value = f"""
                    Verified Date: **{date_}**
**___Time:___** ```ini
[{time_}]
```
WR HOLDER: **{player_}**
Country: **{nation_}**
Length Day: **{duration_}**
**__lap time__** :stopwatch:
:one: {lap1}
:two: {lap2}
:three: {lap3}
<:threemushrooms:1175155099971096679> **{shroom}**
<:item000Coin:1175154443306668192> **{coins}**

**___Combination___**
charecter: **{combo_charecter}** {emoji_character}
vehicle: **{combo_vegicle} {emoji_kart}**
roller: **{combo_roller}  {emoji_tires}**
glider: **{combo_glider} {emoji_glider}**
                """)
            if video_id is not None:
                embed.set_image(url=f"{thumbnail_url}")
            else:
                new_thumbnail = f"https://cdn.discordapp.com/attachments/1172493621732327495/1182027246630866944/image.png?ex=658333a8&is=6570bea8&hm=b4eba452c2b85bd8d744c577725402dcea4a9cedd3813d56a057deba5bb1c3ee&"
                embed.set_image(url=f"{new_thumbnail}")
            embed.set_footer(text="")
            
            if track_url is None:
                embed.set_footer(text="**___The video is not verified yet but you can watch previous wr video**")
                message_edit_1 = await ctx.send(embed=embed)
                
                embed_track_none = MyView(url=track_url, message=message_edit_1,trackname=abbra_track,embed=embed,url150cc=track_url,url200cc=" ")
                
                await message_edit_1.edit(embed=embed, view=embed_track_none)
            else:
                message_edit = await ctx.send(embed=embed)
                yt_send = MyView(url=track_url, message=message_edit,trackname=abbra_track,embed=embed,url150cc=track_url,url200cc=" ")
                 # ส่ง Embed กลับในแชท
                # สร้าง View และ Button หลังจากที่ message_edit ถูกกำหนดค่าแล้ว
                
                await message_edit.edit(embed=embed, view=yt_send)
                
       
        else:
            await ctx.send(result)





        
async def setup(bot):
    await bot.add_cog(mk8dxwr(bot))