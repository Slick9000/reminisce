# reminisce
a discord channel mirroring service. link your servers together.

## what is this
reminisce creates a channel mirroring/universal discord channel, sending the same messages to each server with the channel name `mirror`. 

this was an idea from back in like 2019 by user [hyarsan](https://github.com/hyarsan) and i (originally called reflect) using webhooks, and an extremely efficient version was then made by my friend [superwhiskers](https://github.com/superwhiskers/mirror) in 2022 in an irc style.

i decided to take back up this task for fun and push it as far as possible, and i believe i have done so, adding features such as having the ability to use both styles, the ability to mirror edited messages and a blacklist and report system. 

## invite
it runs through the same bot as [r3ddit](https://github.com/Slick9000/r3dd1t), so you can invite it if you want [here](https://discord.com/oauth2/authorize?client_id=459552609108230158&scope=bot&permissions=8)

## ☕ donations

while completely optional, it would be highly appreciated if you could donate if you like this bot! it can be of any amount.

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://paypal.me/irbee246)

## how to use
get python and `pip install discord.py`, and run reminisce.py

`>enable` (alias `>setup`) will explain the difference between the webhook and irc styling, and allow you to select which version you would want for your guild.

this is indepedent for **every** guild, so if you prefer irc for simplicity reasons and your friend does not, you can use what you prefer without issue.

a channel called `mirror` will be created, and this will be the channel that shares the messages. another user would do the same enable command, and those servers become linked through that channel. reminisce does not listen to any other channels/log anything obviously (plus the code is there, check for yourself)

`>disable`  (alias `>unsetup`) will delete the mirror channel, thus disabling reminisce. you could also disable it by editing the webhook name (webhook) or the channel name (irc), if you wanted to do it manually

`>switch` (alias `>swap`) automatically checks what style you are currently using and swaps to the other style.

`>user` (alias `userlookup`) will look up any users in reminisce. lookups work by username, display name (nickname), or id, and will display the name, nicknames, id and servers the user is in.

using the command without any given context will display your own statistics.

<br/>

the following commands are **administrator only.**

`>blacklist (userid) (reason)` (alias `>bl`, `>ban`) will ban a user from using the mirror channel and add them to the ban list. a dm will be sent explaining the reason for their ban.

using the command without any given context will display all banned users.

`>unblacklist (userid)` (alias `>unbl`, `>unban`) will unban a user, allowing them to use the mirror channel again and removing them from the ban list.

`>report (userid) (reason)` allows a user to report someone else. this report will be sent to the bot owner for review who will determine if a ban is required.

`>help` will display help information

## extra notes
- clean text. no @everyone pings between servers
- message edits are mirrored! fix your spelling errors across all guilds
- reminisce does not mirror bots. this is a security measure, as well as a spam measure
- reminisce has attachment and embed support!
- there is the possibility of ratelimits and thus messages being delayed if many are sent at once. there's really no workaround for this, just the nature of sending several messages through one pipeline. however, i have done all that i can to prevent this from happening
