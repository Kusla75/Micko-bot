import discord
from discord.ext import tasks
import os
from datetime import datetime
from triggers import triggers
import var as v
import module as m

bot = discord.Client()

@bot.event
async def on_ready():
	print(f'{bot.user} successfully started!')

@tasks.loop(hours=1.0)
async def message_of_the_day():
	await bot.wait_until_ready()

	test_channel = bot.get_channel(v.test_channel_ID)
	now = datetime.now()
	if now.hour + 2 == 17:
		await test_channel.send(v.daily_message)
		[trigger.restart_count() for trigger in triggers]
		
@bot.event
async def on_message(message):

	if message.author == bot.user:
		return
	if message.channel.id != v.test_channel_ID:
		return

	if message.content.startswith('-'):
		await message.channel.send('Ova budala mi još nije dala komande')
		## ... ##
		
	else:
		reply = m.check_message_for_trigger(message, triggers)
		if reply != '':
			await message.reply(reply)

message_of_the_day.start()
bot.run(os.getenv('TOKEN'))