# reminisce
another reflect/mirror clone with webhooks

## what is this
using webhooks, reminisce creates a channel mirroring/universal discord channel.

webhooks can be slow due to ratelimits. there's really no workaround for this besides potentially using multiple webhooks and switching when a ratelimit occurs, which is doable, but i have no interest in doing

## how to use
get python and pip install discord.py, and run reminisce.py

**>setup** creates a channel and webhook for the channel called mirror. this is the only setup required for this to work

another user would do the same, and those servers become linked through that channel. reminisce does not listen to any other channels obviously

**>unsetup** will delete the mirror channel. must be run in the channel itself

**>help** will basically display help information

## safeguard features
- clean text. no @everyone pings between servers
- reminisce has attachment support
- reminisce also mirrors bots
