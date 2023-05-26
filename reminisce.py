import discord
from discord.ext import commands
import asyncio
from io import BytesIO

intents = discord.Intents.default()

intents.message_content = True

intents.members = True

bot = commands.Bot(command_prefix=">m ", intents=intents, case_insensitive=True)

bot.remove_command("help")

m = "mirror"


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

        if msg.channel.name == m and channel != msg.channel:

            hook = discord.utils.get(await channel.webhooks(), name = m)

            name = f"{msg.author.display_name} [{msg.guild.name}]"

            if hook:
                
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

                # no image
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
        
    await bot.process_commands(msg)


@bot.command()
async def enable(ctx):

    hook = discord.utils.get(await ctx.channel.webhooks(), name = m)
    
    if hook:
        
        await ctx.send("already setup!")
    
    else:
        
        channel = await ctx.message.guild.create_text_channel(m)
        
        await channel.create_webhook(name = m)
        
        await ctx.send("webhook successfully created.") 
    
        await ctx.send("mirror board created with webhook setup.")

@bot.command()
async def disable(ctx):

    hook = discord.utils.get(await ctx.channel.webhooks(), name = m)

    if hook:

        await ctx.send("shutting down in 5 seconds... thank you for using reminisce!")

        await asyncio.sleep(5)
    
        await hook.channel.delete()

    else:

        await ctx.send("not setup here!")

# setup blacklist feature
# 

@bot.command()
async def user(ctx, user_search):

    try:

        user = discord.utils.get(bot.get_all_members(), id=int(user_search))

    except ValueError:

        user = discord.utils.get(bot.get_all_members(), name=user_search)

        if user == None:

            for guild in bot.guilds:

                for member in guild.members:

                    if user_search == member.display_name:

                        user = discord.utils.get(bot.get_all_members(), id=member.id)

    db = discord.Embed(description="User Lookup")

    db.set_author(name=user.display_name, icon_url=user.avatar)

    db.add_field(name = "Username", value = user.name+user.discriminator)

    db.add_field(name = "ID", value = user.id)

    servers = []

    for guild in bot.guilds:

        for member in guild.members:

            if user == member:

                servers.append(guild.name)


    db.add_field(name = "Servers", value = '\n'.join(str(x) for x in servers))

    await ctx.send(embed=db)


@bot.command()
async def help(ctx):

    db = discord.Embed(title=f"Setup", description="This is reminisce, another server reflection bot using webhooks. Type `>m enable` to setup and `>m disable` to undo setup.")
    
    db.set_author(name=ctx.author, icon_url=ctx.author.avatar)

    await ctx.send(embed=db)


token = open("token.txt").read()

if __name__ == '__main__':

   bot.run(token)
