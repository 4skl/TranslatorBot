import discord, requests
from random import choice

TOKEN = 'TOKEN'
CONTACT_EMAIL = None #'Contact email for getting 10000 words/day instead of 1000'

translate_command = '$t'
id_start = '<@!'

client = discord.Client()

def unescape(text):
    return text.replace('&#39;', '\'').replace('&lt;','<').replace('&gt;', '>') # to improve

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.content.startswith(translate_command):
        lang = message.content[len(translate_command):message.content.find(' ')]
        ttt = message.content[len(translate_command)+len(lang)+1:]
        s = ttt.find(id_start)
        while s != -1:
            e = ttt.find('>',s)
            ttt = ttt[:s]+client.get_user(int(ttt[s+len(id_start):e])).name+ttt[e:]
            s = ttt.find(id_start)
        body = {
            'q': ttt,
            'langpair': lang+'|en' if len(lang) == 2 else lang[:2]+'|'+lang[2:],
            'de': CONTACT_EMAIL
        }
        r = requests.get('https://api.mymemory.translated.net/get', params=body)
        
        message_sent = await message.channel.send(unescape(r.json()['responseData']['translatedText']))
        
        def check(reaction, user):
            return user == message.author and str(reaction.emoji) == '❌'
        
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=600.0, check=check)
        except asyncio.TimeoutError:
            pass
        else:
            await message_sent.delete()

client.run(TOKEN)
