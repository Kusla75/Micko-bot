def check_message_for_trigger(message, triggers):
	responded = False
	reply = ""

	for trigger in triggers:
		if trigger.count > 0 or responded:
			for w in trigger.words:
				if w in message.content.lower():
					trigger.count -= 1
					reply = trigger.response
					responded = True
					break
	
	return reply
