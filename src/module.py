import time as t
import var as v
import discord

def check_message_for_trigger(message, triggers):
	responded = False
	reply = ""

	for trigger in triggers:
		if not responded:
			if trigger.count > 0 and (t.time()-trigger.epoch_t >= v.global_vars["cooldown"]):

				for w in trigger.words:
					if w in message.content.lower():
						trigger.count -= 1
						trigger.epoch_t = t.time()
						reply = trigger.response
						responded = True
						break
	
	return reply

def log_reply(message, reply):
	print(message.channel.name)
	print(message.author.display_name + " - " + message.content)
	print("\t" + reply + "\n")

def check_if_user_has_role(user, allowed_roles):
	roles_ID = [r.id for r in user.roles]
	for r in roles_ID:
		if r in allowed_roles:
			return True
	return False

def set_var(message):
	mess_split = message.content.split(' ')
	if len(mess_split) > 3: return False
	s_variable = mess_split[1]
	try:
		s_value = int(mess_split[2])
	except ValueError:
		return False

	if s_variable in v.global_vars:
		v.global_vars[s_variable] = s_value
		return True
	else:
		return False 

def generate_set_embed(success):
	embed = discord.Embed(description="")
	
	if success:
		embed.description = ":white_check_mark: komanda uspešno izvršena!"
		embed.color = v.green_hex
	else:
		embed.description = ":x: komanda nije izvršena!"
		embed.color = v.red_hex

	return embed

def generate_show_embed():
	embed = discord.Embed(title="Varijable", description="", color=v.blue_hex)

	for key, val in v.global_vars.items():
		embed.description += f"{key}: {val}\n"

	return embed

def generate_embed(desc):
	embed = discord.Embed(description=desc, color=v.blue_hex)
	return embed
