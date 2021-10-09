import discord
from discord.ext import tasks
import os
from datetime import datetime
from triggers import triggers
import var as v
import module as m
from fortunate import Fortunate

bot = discord.Client()
fortune_generator = Fortunate(os.getenv['FORTUNE_FILE'])

@bot.event
async def on_ready():
	print()
	print(f'{bot.user} successfully started!\n')
	print("Logs: \n")

@tasks.loop(hours=1.0)
async def message_of_the_day():
	await bot.wait_until_ready()

	channel = bot.get_channel(v.test_channel_ID)
	now = datetime.now()
	if now.hour + 2 == v.global_vars['daily_message_hour']:
		await channel.send(v.daily_message)
		[trigger.restart_count() for trigger in triggers]
	if now.hour + 2 == v.global_vars['fortune_message_hour']:
		await channel.send(fortune_generator())
	
		
@bot.event
async def on_message(message):

	print(fortune_generator())
	if message.author == bot.user:
		return
	if message.channel.id != v.test_channel_ID:
		return

	if message.content.startswith('-'):

		if message.content.startswith('-help'):
			await message.reply('Nema ti pomoći buraz!')
		else:
			is_allowed = m.check_if_user_has_role(message.author, v.allowed_roles)
			
			if message.content.startswith('-set') and is_allowed:
				embed_reply = m.generate_set_embed(m.set_var(message))
				await message.channel.send(embed=embed_reply)

			elif message.content.startswith('-show') and is_allowed:
				embed_reply = m.generate_show_embed();
				await message.channel.send(embed=embed_reply)

			elif message.content.startswith('-quit') and is_allowed:
				embed_reply = m.generate_embed("Idem u večiti san... :sleeping:")
				await message.channel.send(embed=embed_reply)
				print(f"Shutting down {bot.user}\n")
				await bot.close()

			else:
				if not is_allowed:
					await message.reply(v.not_allowed_mess)
				else:
					await message.reply(v.unknown_command)
			
	else:
		reply = m.check_message_for_trigger(message, triggers)
		if reply != '':
			await message.reply(reply)
			m.log_reply(message, reply)

message_of_the_day.start()
bot.run(os.getenv('TOKEN'))