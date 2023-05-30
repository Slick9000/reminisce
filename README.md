# reminisce
a reflect/mirror clone with the unique ability to select between webhook and irc style mirroring, indepedent for each guild.

## what is this
reminisce creates a channel mirroring/universal discord channel, sending the same messages to each server with the channel name `mirror`. 

this was an idea from back in like 2019 by user hyarsan and i (originally called reflect), however an extremely efficient version was then made by my friend [superwhiskers](https://github.com/superwhiskers/mirror) in 2022.

i decided to take back up this task for fun, and really push the idea as far as it can go

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

`>blacklist (userid)` (alias `>bl`, `>ban`) will ban a user from using the mirror channel and add them to the ban list. a dm will be sent explaining the reason for their ban.

using the command without any given context will display all banned users.

`>unblacklist (userid)` (alias `>unbl`, `>unban`) will unban a user, allowing them to use the mirror channel again and removing them from the ban list.

`>help` will display help information

## extra notes
- clean text. no @everyone pings between servers
- reminisce has attachment support
- reminisce does not mirror bots. this is partially due to the way it works altogether but doubles as a safety measure.
- webhooks can be slow due to ratelimits. there's really no workaround for this besides potentially using multiple webhooks and switching when a ratelimit occurs, but that could be strange to setup and i have no interest in doing it
- 
