import discord
import os
from triggers import triggers
from var import test_channel_ID
import module as m

bot = discord.Client()

@bot.event
async def on_ready():
	print('{0} successfully started!'.format(bot.user))

@bot.event
async def on_message(message):

	if message.author == bot.user:
		return

	if message.channel != bot.get_channel(test_channel_ID):
		return

	if message.content.startswith('-'):
		await message.channel.send('Ova budala mi još nije dala komande')
	else:
		reply = m.check_message_for_trigger(message, triggers)
		if reply != "":
			await message.channel.send(reply)

bot.run(os.getenv('TOKEN'))