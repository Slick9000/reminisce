import asyncio
import discord
from discord.ext import commands
from io import BytesIO
import json
import os

intents = discord.Intents.default()

intents.message_content = True

intents.members = True

bot = commands.Bot(command_prefix=">", intents=intents, case_insensitive=True)

bot.remove_command("help")

m = "mirror"

blacklist_file = f"{os.path.dirname(os.path.abspath(__file__))}/blacklist.json"


@bot.event
async def on_ready():

    print(f"Connected and logging events.")


@bot.event
async def on_message(msg):

    channel_list = []

    for guild in bot.guilds:
    
        for channel in guild.text_channels:

            if channel.name == m:
    
                channel_list.append(channel)

    for channel in channel_list:

        if isinstance(msg.channel, discord.channel.DMChannel):
            
            return

        if msg.channel.name == m and channel != msg.channel:

            if os.path.exists(blacklist_file):

                with open(blacklist_file) as read_file:
                
                    data = json.load(read_file)

                    users = data[0]['users']

                    for i in range(len(users)):

                        if str(msg.author.id) == users[i]['id']:

                            user = discord.utils.get(bot.get_all_members(), name=msg.author.name)

                            banned_embed = discord.Embed(title=f"Banned", description=f"**Reason:** {users[i]['reason']}")

                            banned_embed.add_field(name = "Username", value = user)

                            banned_embed.set_author(name=user.name, icon_url=user.avatar)

                            await user.send(embed=banned_embed)

                            return

            hook = discord.utils.get(await channel.webhooks(), name = m)

            name = f"{msg.author.display_name} [{msg.guild.name}]"

            if hook:

                if msg.author == bot.user:

                        return
                    
                if msg.webhook_id:

                    return

                if msg.embeds:

                    send_embeds = list(msg.embeds)

                    await hook.send(
                        content    = msg.clean_content,
                        embeds     = send_embeds,
                        username   = name,
                        avatar_url = msg.author.avatar
                    )

                elif msg.attachments == []:

                    await hook.send(
                        content    = msg.clean_content,
                        username   = name,
                        avatar_url = msg.author.avatar
                        )
                    
                else:

                    fp = BytesIO()

                    attachment = msg.attachments[0]

                    await attachment.save(fp)
                    
                    send_file = discord.File(fp = fp, filename = attachment.filename)

                    await hook.send(
                        content    = msg.clean_content,
                        file      = send_file,
                        username   = name,
                        avatar_url = msg.author.avatar
                        )
                        
            else:

                if msg.author == bot.user:

                    return
                
                if msg.webhook_id:

                    return

                if msg.embeds:

                    send_embeds = list(msg.embeds)

                    await channel.send(f"**{name}:** {msg.clean_content}", embeds = send_embeds)

                elif msg.attachments == []:
                    
                    await channel.send(f"**{name}:** {msg.clean_content}")

                else:

                    fp = BytesIO()

                    attachment = msg.attachments[0]

                    await attachment.save(fp)
                    
                    send_file = discord.File(fp = fp, filename = attachment.filename)

                    await channel.send(f"**{name}:** {msg.clean_content}", file = send_file)
        
    await bot.process_commands(msg)


@bot.command(aliases=["setup"])
async def enable(ctx):

    if not ctx.message.author.guild_permissions.administrator:

        await ctx.send("Only server admins can use this command.")

        return

    reactions = ['1️⃣', '2️⃣']
    
    selection = discord.Embed(description="**Setup**")

    selection.add_field(name = "Make a decision!", value = """Reminisce has two options - Webhook and IRC setup.

    **Webhook setup** will look the most natural - styled to look like regular Discord chats.

    **IRC mode** styles in classic, text only style similar to the likes of 4chan.

    The image below is an example.

    Select **reaction 1** to use Webhooks.
    
    Select **option 2 to use IRC**. You can change this at any time.
    """)

    selection.set_image(url="https://media.discordapp.net/attachments/440634457234341925/1112991175259996252/image.png?width=459&height=172")

    choice = await ctx.send(embed=selection)

    for option in reactions:

        await choice.add_reaction(option)

    def check(reaction, user):

        return user == ctx.author and str(reaction.emoji) in reactions

    try:

        reaction, user = await bot.wait_for('reaction_add', timeout=20.0, check=check)

    except asyncio.TimeoutError:

        await ctx.channel.send('Took too long to react, please try again!')

    else:

        await choice.clear_reactions()

        i = reactions.index(str(reaction))

        if i == 0:

            hook = discord.utils.get(await ctx.channel.webhooks(), name = m)
            
            if hook:
                
                await ctx.send("Reminisce is already setup!")
            
            else:
                
                channel = await ctx.message.guild.create_text_channel(m)

                await channel.edit(topic="**Help: >help**")
                
                await channel.create_webhook(name = m)
                
                await ctx.send("Webhook successfully created.") 
            
                await ctx.send("Mirror channel created with **webhook** setup.")

        if i == 1:

            channel = await ctx.message.guild.create_text_channel(m)

            await channel.edit(topic="**Help: >help**")

            await ctx.send("Mirror channel created with **IRC** setup.")


@bot.command(aliases=["unsetup"])
async def disable(ctx):

    if not ctx.message.author.guild_permissions.administrator:

        await ctx.send("Only server admins can use this command.")

        return

    channel = discord.utils.get(ctx.guild.channels, name = m)

    if channel:

        await ctx.send("Shutting down... thank you for using reminisce!")

        await asyncio.sleep(2)
    
        await channel.delete()

        await ctx.send("Reminisce has been shut down.")

    else:

        await ctx.send("Reminisce is not setup!")


@bot.command(aliases=["swap"])
async def switch(ctx):

    if not ctx.message.author.guild_permissions.administrator:

        await ctx.send("Only server admins can use this command.")

        return

    hook = discord.utils.get(await ctx.guild.webhooks(), name = m)

    if hook:

        await hook.delete()

        await ctx.send("Reminisce has switched to **IRC** method!")

    else:

        channel = discord.utils.get(ctx.guild.channels, name = m)

        await channel.create_webhook(name = m)

        await ctx.send("Reminisce has switched to **Webhook** method!")


@bot.command(aliases=["userlookup"])
async def user(ctx, *, user_search = None):

    servers = []

    nicknames = []

    user_type = 0

    if user_search == None:

        user = discord.utils.get(bot.get_all_members(), name=ctx.author.name)
    
    else:

        try:

            user = discord.utils.get(bot.get_all_members(), id=int(user_search))

        except ValueError:

            user_type = 1

            user = discord.utils.get(bot.get_all_members(), name=user_search)

            if user == None:

                for guild in bot.guilds:

                    for member in guild.members:

                        if user_search == member.nick:

                            user = discord.utils.get(bot.get_all_members(), id=member.id)

        if user == None:

            await ctx.send("User does not exist!")
                
            return
    
    for guild in bot.guilds:

        for member in guild.members:

            if user == member:

                nicknames.append(member.nick)
                
                servers.append(guild.name)

    user_info = discord.Embed(description="User Lookup")

    user_info.set_author(name=user.name if user_type == 0 else user_search, icon_url=user.avatar)

    user_info.add_field(name = "Username", value = user)

    user_info.add_field(name = "Nicknames", value = '\n'.join(str(x) for x in nicknames))

    user_info.add_field(name = "ID", value = user.id)

    user_info.add_field(name = "Servers", value = '\n'.join(str(x) for x in servers))

    await ctx.send(embed=user_info)


@bot.command()
async def report(ctx, user_search = None, *, reason = None):

    #hardcoded my id as discord does not have a call to send to bot owner.
    owner = discord.utils.get(bot.get_all_members(), id=357641367507435531)

    if user_search == None:

        await ctx.send("Please specify a user by ID! This can be found using `>user (name)`")
    
    else:

        reported_user = discord.utils.get(bot.get_all_members(), id=int(user_search))
    
        if user == None:

            await ctx.send("User does not exist!")
                
            return

    report = discord.Embed(description="**Report**")

    report.set_author(name=reported_user, icon_url = reported_user.avatar)

    report.add_field(name = "Reason", value = reason)

    report.add_field(name = "Submitted By", value = ctx.author)

    await owner.send(embed = report)


@bot.command(aliases=["bl", "ban"])
@commands.is_owner()
async def blacklist(ctx, userid = None, *, reason = None):

    if os.path.exists(blacklist_file):

        with open(blacklist_file) as read_file:
        
            data = json.load(read_file)

            users = data[0]['users']

            if userid == None:
                
                banned = ""

                reasons = ""

                for i in range(len(users)):

                    banned += f"({i+1}) {users[i]['name']}\n"

                    reasons += f"({i+1}) {users[i]['reason']}\n"

                resp = discord.Embed(title=f"Blacklisted Users")

                resp.add_field(name = "Users", value = banned)

                resp.add_field(name = "Reasons", value = reasons)

                await ctx.send(embed=resp)

                return
            
            for i in range(len(users)):

                if userid == users[i]['id']:

                    user = discord.utils.get(bot.get_all_members(), id=int(userid))

                    resp = discord.Embed(title=f"User **{user}** already blacklisted!", description=f"**Reason:** {users[i]['reason']}")
                    
                    resp.set_author(name=user.name, icon_url=user.avatar)

                    await ctx.send(embed=resp)

                    return

            else:

                user = discord.utils.get(bot.get_all_members(), id=int(userid))

                try:
                
                    data[0]['users'].append({"id" : userid, "name": user.name, "reason": reason})

                except AttributeError:

                    await ctx.send("Invalid User ID.")

                    return
                
                with open(blacklist_file, "w") as create_file:
    
                    json.dump(data, create_file, indent=4)

                    await ctx.send(f"User {user} blacklisted!")

    else:

        if userid == None:

            await ctx.send("Provide a User ID to populate the list! (No users blacklisted)")

            return

        user = discord.utils.get(bot.get_all_members(), id=int(userid))

        try:
            
            add_user = [{"users": [{"id" : userid, "name": user.name, "reason": reason}]}]

        except AttributeError:

            await ctx.send("Invalid User ID.")

            return
        
        with open(blacklist_file, "w") as create_file:
        
            json.dump(add_user, create_file, indent=4)

        await ctx.send(f"User {user} blacklisted!")

@bot.command(aliases=["unbl", "unban"])
@commands.is_owner()
async def unblacklist(ctx, userid = None):

    if os.path.exists(blacklist_file):

        with open(blacklist_file) as read_file:
        
            data = json.load(read_file)

            users = data[0]['users']

            if userid == None:

                await ctx.send("Please provide a User ID!")

                return
        
            for i in range(len(users)):

                if userid == users[i]['id']:

                    data.pop(i)

                    if data == []:

                        read_file.close()

                        os.remove(blacklist_file)

                    else:

                        with open(blacklist_file, "w") as create_file:
        
                            json.dump(data, create_file, indent=4)

                    user = discord.utils.get(bot.get_all_members(), id=int(userid))

                    resp = discord.Embed(title=f"User Unbanned", description=f"{user} has been unbanned!")
                    
                    resp.set_author(name=user.name, icon_url=user.avatar)

                    await ctx.send(embed=resp)

                    return
                
    else:

        await ctx.send("No banned users!")


@bot.command()
async def help(ctx):

    help = discord.Embed(title=f"Help", description="This is reminisce, another server mirroring bot using webhooks.")
    
    help.add_field(name = "Server Admin Commands", value = """`>enable` (alias `>setup`) to setup. It will ask you whether you want webhook or IRC style, and you will select it with 
    Reaction 1️⃣ (webhook) or 2️⃣ (IRC)

    `>disable` (alias `>unsetup`) to undo setup.

    `>switch` (alias `>swap`) automatically determines which style you use, and switches it if you desire.
    """)

    help.add_field(name = "General User Commands", value = """`>user` (alias `>userlookup`) will lookup a user (works by username, nickname, or id)

    `>report (user) (reason)` will send a dm reporting the user to the administrator.
    """)
    
    help.add_field(name = "Owner Commands", value = """Bot Owner Only Commands

    `>blacklist (userid) (reason)` (alias `>bl`, `>ban`) will ban a user from using the mirror channel and add them to the ban list. 
    A DM will be sent explaining the reason for their ban.
    `>blacklist` by itself (without userid) will bring up the entire list of banned users.
    
    `>unblacklist (userid)` (alias `>unbl`, `>unban`) will unban a user, allowing them to use the mirror channel again and removing them from the ban list.
    Have fun!
    """)

    await ctx.send(embed=help)


token = open("token.txt").read()

if __name__ == '__main__':

   bot.run(token)
