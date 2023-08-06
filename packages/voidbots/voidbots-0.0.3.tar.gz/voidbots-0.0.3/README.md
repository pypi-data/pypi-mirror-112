
## Installation
`pip install voidbots`

## Documentation
To see the Doc [click here](https://docs.voidbots.net/).

Before using this module, Please view [Ratelimits](https://docs.voidbots.net/#/ratelimits) and [Caching](https://docs.voidbots.net/#/caching).

## Example
```
import voidbots as vd
from discord.ext.commands import Bot

bot = Bot(command_prefix='vd!')
# Functions
Void = vd.VoidClient(bot, apikey='Your api key')
await Void.get_voteinfo('A bot id','A user id')
await Void.get_botinfo('A bot id')
await Void.postStats(bot.user.id, len(bot.guilds), bot.shard_count or 0)
await Void.get_analytics(bot.user.id)
await Void.get_reviews(bot.user.id)
await Void.widget(bot.user.id, theme='dark or light')
await Void.get_userinfo("A user id")
await Void.get_pack("The pack id")
#This is just examples , it should work.
```