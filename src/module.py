import time as t
import var as v
import discord
import os
import random as r
import hashlib
from urllib.request import urlopen, Request
import requests


def get_fortune():
    fortunes = ''

    with open(os.getenv('FORTUNE_FILE'), 'r') as f:
        for line in f.readlines():
            fortunes += line
        fortunes = fortunes.split('%\n')
    
    rand_index = r.randint(0, len(fortunes)-1)
    return '\n' + fortunes[rand_index]

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

def generate_embed(t='', desc=''):
	embed = discord.Embed(title=t, description=desc, color=v.blue_hex)
	return embed

def bodovi(message):
	bodovi = message.content.split(" ")
	bodovi = bodovi[1:]

	prosek = 0
	for b in bodovi:
		if(int(b) < 0 or int(b) > 100):
			return "Sigurno nemaš ovoliko bodova :neutral_face:"
		else:
			prosek += int(b)
	prosek = prosek / len(bodovi)		

	konacno = 0
	if(prosek >= 40):
		konacno = 49/60 * prosek + 55/3
		konacno = round(konacno, 2)
		mess = str(konacno) + " bodova\n"
	elif(prosek < 40):
		return "Brate moj nisi ti tu algebru položio :cry:"
	else:
		return "Doslo je do greske pri racunanju bodova!"
	
	mess += "Ocena: "
	if(konacno >= 91):
		mess += ":keycap_ten:"
	elif(konacno < 91 and konacno >= 81):
		mess += ":nine:" 
	elif(konacno < 81 and konacno >= 71):
		mess += ":eight:" 
	elif(konacno < 71 and konacno >= 61):
		mess += ":seven:" 
	elif(konacno < 61 and konacno >= 51):
		mess += ":six:"
	else:
		pass

	return mess

# def check_site_changes():
# 	if v.tracked_sites_size == []:
# 		for i, link in enumerate(v.tracked_sites):
# 			request = urlopen(link)
# 			v.tracked_sites_size.append(len(request.read()))
# 			t.sleep(10)
# 			return False
# 	else:
# 		for i, link in enumerate(v.tracked_sites):
# 			request = urlopen(link)
# 			new_length = len(request.read())

# 			if abs(v.tracked_sites_size[i]-new_length) > 450:
# 				v.tracked_sites_size[i] = new_length
# 				return True
# 			else:
# 				v.tracked_sites_size[i] = new_length
# 				return False
