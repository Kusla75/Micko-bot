import discord
from discord.ext import tasks
import os
from datetime import datetime
from triggers import triggers
import var as v
import module as m
from alive import keep_alive

bot = discord.Client()

@bot.event
async def on_ready():
	print()
	print(f'{bot.user} successfully started!\n')
	print("Logs: \n")
	await bot.change_presence(activity=discord.Game(name="-help"))


@tasks.loop(hours=1.0)
async def message_of_the_day():
	await bot.wait_until_ready()

	channel = bot.get_channel(v.main_chat_ID)
	now = datetime.now()

	if now.hour + 2 == v.global_vars['daily_message_hour']:
		await channel.send(v.daily_message)
		[trigger.restart_count() for trigger in triggers]

	if now.hour + 2 == v.global_vars['fortune_message_hour']:
		fortune_embed = m.generate_embed('Mudrolija dana :scroll:', m.get_fortune())
		await channel.send(embed=fortune_embed)
		
	
@bot.event
async def on_message(message):

	if message.author == bot.user:
		return
	# if message.channel.id != v.test_channel_ID:
	# 	return

	if message.content.startswith('-'):

		if message.content.startswith('-help'):
			await message.reply('Nema ti pomoći buraz!')
		else:
			is_allowed = m.check_if_user_has_role(message.author, v.allowed_roles)
			
			if message.content.startswith('-set') and is_allowed:
				embed_reply = m.generate_set_embed(m.set_var(message))
				await message.channel.send(embed=embed_reply)

			elif message.content.startswith('-restart') and is_allowed:
				[trigger.restart_count() for trigger in triggers]
				await message.channel.send(embed=m.generate_set_embed(True))

			elif message.content.startswith('-show'):
				embed_reply = m.generate_show_embed();
				await message.channel.send(embed=embed_reply)

			# elif message.content.startswith('-fortune') and is_allowed:
			# 	embed_reply = m.generate_embed('Mudrolija :scroll:', m.get_fortune())
			# 	await message.channel.send(embed=embed_reply)

			elif message.content.startswith('-quit') and is_allowed:
				embed_reply = m.generate_embed(desc="Idem u večiti san... :sleeping:")
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

keep_alive()
os.system('clear')
message_of_the_day.start()
bot.run(os.getenv('TOKEN'))