# reminisce
another reflect/mirror clone with webhooks

## what is this
using webhooks, reminisce creates a channel mirroring/universal discord channel.

## how to use
get python and pip install discord.py, and run reminisce.py

**>rem enable** creates a channel and webhook for the channel called mirror. this is the only setup required for this to work

another user would do the same, and those servers become linked through that channel. reminisce does not listen to any other channels obviously

**>rem disable** will delete the mirror channel. must be run in the channel itself

**>rem user** will look up users in reminisce! (or moreso, any users the bot is in)

lookups work by username, display name (nickname), or id, and will display the servers the user is in.

**>rehelp** will basically display help information

## extra notes
- clean text. no @everyone pings between servers
- reminisce has attachment support
- reminisce mirrors bots
- blacklisting is planned but currently unsupported
- webhooks can be slow due to ratelimits. there's really no workaround for this besides potentially using multiple webhooks and switching when a ratelimit occurs, but that could be strange to setup and i have no interest in doing it
