import time as t
from triggers import cooldown

def check_message_for_trigger(message, triggers):
	responded = False
	reply = ""

	for trigger in triggers:
		if not responded:
			if trigger.count > 0 and (t.time()-trigger.epoch_t >= cooldown):

				for w in trigger.words:
					if w in message.content.lower():
						trigger.count -= 1
						trigger.epoch_t = t.time()
						reply = trigger.response
						responded = True
						break
	
	return reply
