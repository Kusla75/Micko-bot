import discord
import os
from triggers import *

client = discord.Client()

@client.event
async def on_ready():
    print('{0.user} successfully started'.format(client))

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return

    if message.content.startswith('-'):
        await message.channel.send('Ova budala mi još nije dala komande')
    else:
        for ind, trigger_tuple in enumerate(triggers):
            for t in trigger_tuple:
                if t in message.content.lower():
                    await message.channel.send(response[ind])
                    break
            

client.run(os.getenv('TOKEN'))