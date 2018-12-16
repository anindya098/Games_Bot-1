
import telegram
import logging, random, os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import league as lg
import strings
import fortnite as fnite

TOKEN = os.getenv('GAMES_BOT_TOKEN')



def start(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Beep Beep Boop! I am a bot!")

def echo(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def help(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="I am poorly programmed and cannot help :(")

def stats(bot, update, args):

	summoner_name = ""
	msg_ID = update.message.message_id

	for i in args:
		summoner_name = summoner_name + i + " "
	
	reply = ""
	champ_mastery_result = lg.getChampMastery(summoner_name)
	count = 0
	for champ in champ_mastery_result[0]:
		reply += champ + " - " + str(champ_mastery_result[1][count]) + "\n"
		count += 1
	if(len(reply) <= 0):
		reply = "Get a champ to level 7 you moron"
	bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=lg.getChampMastery(summoner_name))
	bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=reply)

def league(bot, update):
	msg_ID = update.message.message_id
	question = "@SaveTheBeeees @DankMemesCanMeltSteelBeams @hotterthanahotdog @bleachonmytshirt @Insolent_child league?"
	bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)

def fortnite(bot, update, args):
	msg_ID = update.message.message_id
	if not args:
		question = "@TheBoneDoctor @prankpatrol @Insolent_child @bleachonmytshirt @AtraWolf @hotterthanahotdog @SaveTheBeeees fortnite?"
		bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)

	elif (len(args) == 1 and args[0] == "shop"):
		bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text="Let me open the shop up! One second please.")
		resp = fnite.getWeeklyStore()
		bot.send_media_group(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, media=resp)
		resp = fnite.getDailyStore()
		bot.send_media_group(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, media=resp)
	elif (len(args) == 1 and args[0] == "challenges"):
		bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text="Let me check the challenges")
		resp = fnite.getChallenges()
		bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=resp)
	else:
		name = ""
		for word in args:
			name = name + word + " "

		resp = fnite.getStats(name)
		bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=resp)

def overwatch(bot, update):		
	msg_ID = update.message.message_id
	question = "@SaveTheBeeees @DankMemesCanMeltSteelBeams @hotterthanahotdog @bleachonmytshirt @prankpatrol @AtraWolf Overwatch?"
	bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)

def forest(bot, update):
	msg_ID = update.message.message_id
	question = "@prankpatrol @Insolent_child @AtraWolf @SaveTheBeeees @DankMemesCanMeltSteelBeams forest?"
	bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)

def dauntless(bot, update):
	msg_ID = update.message.message_id
	question = "@prankpatrol @Insolent_child @AtraWolf @SaveTheBeeees @DankMemesCanMeltSteelBeams dauntless?"
	bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)

#Function that reads the chat, and if a user says certain words it will interrupt.
def interjection(bot, update):
	from_user = update.message.from_user.first_name
	msg_ID = update.message.message_id
	msg_text = update.message.text.lower()
	msg_lst = msg_text.split()

	#bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=from_user)
	#If Kalada says the word yi, then reply
	if(from_user == "Kalada" and "yi" in msg_lst):
		i = random.randrange(len(strings.master_yi))
		reply = strings.master_yi[i]
		bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=reply)

	if(from_user == "Hardeep" and "for honor" in msg_lst):
		reply = "Dead Game"
		bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=reply)


def unknown(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Sorry I didn't understand that command. :(")

def caps(bot, update, args):
	text_caps = ' '.join(args).upper()
	bot.send_message(chat_id=update.message.chat_id, text=text_caps)


def main():
	bot = telegram.Bot(token=TOKEN)
	updater = Updater(token=TOKEN)
	dispatcher = updater.dispatcher
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

	#echo_handler = MessageHandler(Filters.text, echo)
	start_handler = CommandHandler('start', start)
	help_handler = CommandHandler('help', help)
	caps_handler = CommandHandler('caps', caps, pass_args=True)
	stats_handler = CommandHandler('stats', stats, pass_args=True)
	league_handler = CommandHandler('league', league)
	fortnite_handler = CommandHandler('fortnite', fortnite, pass_args=True)
	overwatch_handler = CommandHandler('overwatch', overwatch)
	forest_handler = CommandHandler('forest', forest)
	dauntless_handler = CommandHandler('dauntless', dauntless)
	interjection_handler = MessageHandler(Filters.all, interjection)

	unknown_handler = MessageHandler(Filters.command, unknown)


	#dispatcher.add_handler(echo_handler)
	dispatcher.add_handler(start_handler)
	dispatcher.add_handler(help_handler)
	dispatcher.add_handler(caps_handler)
	dispatcher.add_handler(stats_handler)
	dispatcher.add_handler(league_handler)
	dispatcher.add_handler(fortnite_handler)
	dispatcher.add_handler(overwatch_handler)
	dispatcher.add_handler(forest_handler)
	dispatcher.add_handler(dauntless_handler)

	dispatcher.add_handler(interjection_handler)	
	dispatcher.add_handler(unknown_handler)

	updater.start_polling()

main()

