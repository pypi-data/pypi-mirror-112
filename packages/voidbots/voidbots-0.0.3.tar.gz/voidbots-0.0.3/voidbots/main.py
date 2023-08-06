import aiohttp, asyncio
import html
import discord
from asyncio.tasks import Task
class VoidClient:
    def __init__(self, bot: discord.Client, apikey: str, autopost: bool =False, **kwargs):
        self.base_url = 'https://api.voidbots.net'
        self.apikey = apikey
        self.bot = bot
        self._autopost = autopost
        self.module_closed = False
        self.task_auto_post = Task
        self.loop = kwargs.get('loop', bot.loop)
        
        if self._autopost:
            self.task_auto_post = self.loop.create_task(self.__auto_post__())
        
        
    async def __auto_post__(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            try:
                await self.postStats(self.bot.user.id, len(self.bot.guilds), self.bot.shard_count)
            except Exception:
                pass
            await asyncio.sleep(210)
    
    async def get_voteinfo(self, bot_id: int, user_id: int):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.base_url}/bot/voted/{bot_id}/{user_id}', headers={'Authorization': self.apikey}) as req:
                req = await req.json()
        return {'endpoint': f'{self.base_url}/bot/voted', 'rep': html.unescape(req)}
    
    async def get_botinfo(self, bot_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.base_url}/bot/info/{bot_id}', headers={'Authorization': self.apikey}) as req:
                req = await req.json()
        return {'endpoint': f'{self.base_url}/bot/info', 'rep': html.unescape(req)}
    
    async def postStats(self, bot_id, server_count: int, shard_count: int=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.base_url}/bot/stats/{bot_id}',
                                   headers={'Authorization': self.apikey}, json={'server_count': server_count, 'shard_count': shard_count or 0}) as req:
                req = await req.json()
        return {'endpoint': f'{self.base_url}/bot/analytics', 'rep': html.unescape(req)}
    
    async def get_analytics(self, bot_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.base_url}/bot/analytics/{bot_id}', headers={'Authorization': self.apikey}) as req:
                req = await req.json()
        return {'endpoint': f'{self.base_url}/bot/analytics', 'rep': html.unescape(req)}
        
    async def get_reviews(self, bot_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.base_url}/bot/reviews/{bot_id}', headers={'Authorization': self.apikey}) as req:
                req = await req.json()
        return {'endpoint': f'{self.base_url}/bot/reviews', 'rep': html.unescape(req)}
    
    async def widget(self, bot_id, theme=None):
        if theme == None:
            theme = 'dark'
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://voidbots.net/api/embed/{bot_id}?theme={theme}') as req:
                req = await req.json()     
        return {"endpoint": 'https://voidbots.net/api/embed', 'rep': html.unescape(req)}

    async def search(self, *, query=None):
        if query == None:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{self.base_url}/bot/search', headers={'Authorization': self.apikey}) as req:
                    req = await req.json()
            return {'endpoint': f'{self.base_url}/bot/search', 'rep': html.unescape(req)}
        if query is not None:
            try:
                query.replace(" ", "&")
            except Exception:
                pass
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{self.base_url}/search/{query}', headers={'Authorization': self.apikey}) as req:
                    req = await req.json()
            return {'endpoint': f'{self.base_url}/search', 'rep': html.unescape(req)}
    async def get_userinfo(self, user_id: int):
        async with aiohttp.ClientSession() as session:
                async with session.get(f'{self.base_url}/user/info/{user_id}', headers={'Authorization': self.apikey}) as req:
                    req = await req.json()
        return {'endpoint': f'{self.base_url}/user/info', 'rep': html.unescape(req)}
    async def get_pack(self, pack_id: int):
        async with aiohttp.ClientSession() as session:
                async with session.get(f'{self.base_url}/pack/info/{pack_id}', headers={'Authorization': self.apikey}) as req:
                    req = await req.json()
        return {'endpoint': f'{self.base_url}/pack/info', 'rep': html.unescape(req)}
    async def close(self):
        if self.module_closed == True:
            return
        else:
            if self._autopost:
                self.task_auto_post.cancel()
            self.module_closed = True
