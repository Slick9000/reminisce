import discord
from discord.ext import commands
import asyncio
from io import BytesIO

intents = discord.Intents.default()

intents.message_content = True

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

            if hook:
                
                if msg.webhook_id:

                    return

                if msg.embeds:

                    send_embeds = list(msg.embeds)

                    await hook.send(
                        content    = msg.clean_content,
                        embeds     = send_embeds,
                        username   = msg.author.display_name,
                        avatar_url = msg.author.avatar
                    )

                # no image
                elif msg.attachments == []:

                    await hook.send(
                        content    = msg.clean_content,
                        username   = msg.author.display_name,
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
                        username   = msg.author.display_name,
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

@bot.command()
async def help(ctx):

    db = discord.Embed(title=f"Setup", description="This is reminisce, another server reflection bot using webhooks. Type `>m setup` to setup and `>m unsetup` to undo setup.")
    
    db.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar)

    await ctx.send(embed=db)


token = open("token.txt").read()

if __name__ == '__main__':

   bot.run(token)
