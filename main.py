"""
This is the main file for the bot, this is the file that must be run for the bot to work. MOST of the methods in this file coorespond to different commands that the bot can handle
Docs for the Telegram Bot API: https://python-telegram-bot.readthedocs.io/en/stable/index.html
"""

import telegram
import logging, random, os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import league as lg
import strings
import fortnite as fnite
import apex as apx

#Telegram gives each bot a specific identifier or token that is required for it to work
TOKEN = os.getenv('GAMES_BOT_TOKEN')

#command /start sends a message
def start(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Beep Beep Boop! I am a bot!")

#command /help sends a funny reply that isn't that helpful
def help(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="I am poorly programmed and cannot help :(")

#command /stats [name] sends back info on the most played champions in League of Legends for the name given
def stats(bot, update, args):
	summoner_name = ""
	
	#msg_ID is the ID of the message that called the command, this is used so the bot can reply to the specific message
	msg_ID = update.message.message_id

	#args given after the command are given as a list, this basically forms the players name if there were spaces in it
	for i in args:
		summoner_name = summoner_name + i + " "
	
	reply = ""
	
	#getChampMastery(summoner_name) returns a tuple with info regarding a players most played champs (found in league.py)
	#The tuple looks like ([list of champions], [list of mastery points])
	champ_mastery_result = lg.getChampMastery(summoner_name)
	count = 0
	#For each champion (up to 5), add to a string their name and the points the player has on them.
	for champ in champ_mastery_result[0]:
		reply += champ + " - " + str(champ_mastery_result[1][count]) + "\n"
		count += 1
	if(len(reply) <= 0):
		reply = "Wow, something went wrong!"
	
	#Bot replies to the message with the command with the reply string
	bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=reply)

#command /match [name] sends back an image detailing the players and champions in the specified players League of Legends game. (This command takes a while to finish, but can be fixed)
def match(bot, update, args):
	summoner_name = ""
	msg_ID = update.message.message_id
	for i in args:
		summoner_name = summoner_name + i + " "

	#Bot sends a message saying that it is working on the request
	bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text="Let me login and check the game! One second")
	
	#Calls a method that will modify an image that the bot will send. (method found in league.py)
	lg.getCurrentGame(summoner_name)

	#The image being modified is saved to disk, so once the method above is finished the bot can send the file, and telegram takes care of the rest
	bot.send_photo(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, photo=open("tesload.png", 'rb'))

#command /league makes the bot tag everyone in the chat that plays League of Legends by their telegram username
def league(bot, update, args):
	msg_ID = update.message.message_id
	if not args:
		question = "@SaveTheBeeees @anobdya @hotterthanahotdog @weloseifsejuanidoesntgank @TheKidThatOutRanEkko @Insolent_child @Atrawolf @bleachonmytshirt league?"
		bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)
	else:
		summoner_name = ""
		for i in args:
			summoner_name = summoner_name + i + " "

		bot.send_message(parse_mode='MARKDOWN', chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text="beep boop one sec")
		ranked_stats = lg.getAllStats(summoner_name)
		bot.send_chat_action(chat_id=update.message.chat_id, action="UPLOAD_PHOTO")
		bot.send_photo(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, photo=open("statstest.png", 'rb'))

#command /dota makes the bot tag everyone in the chat that plays Dota by their telegram username
def dota(bot, update):
	msg_ID = update.message.message_id
	question = "@Insolent_child @AtraWolf @prankpatrol dota?"
	bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)

#command /ror makes the bot tag everyone in the chat that plays Risk of Rain by their telegram username
def ror(bot, update):
	msg_ID = update.message.message_id
	question = "@SaveTheBeeees @anobdya @AtraWolf @prankpatrol Risk of Rain 2?"
	bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)

#command /ror makes the bot tag everyone in the chat that plays Risk of Rain by their telegram username
def r6(bot, update):
	msg_ID = update.message.message_id
	question = "@SaveTheBeeees @anobdya @Insolent_child @AtraWolf @prankpatrol @bleachonmytshirt R6 Siege?"
	bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)
	
#command /fortnite can take optional arguments
def fortnite(bot, update, args):
	msg_ID = update.message.message_id

	#command /fortnite makes the bot tag everyone in the chat that plays Fortnite by their telegram username
	if not args:
		question = "@TheBoneDoctor @prankpatrol @Insolent_child @bleachonmytshirt @AtraWolf @hotterthanahotdog @SaveTheBeeees fortnite?"
		bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)

	#command /fortnite shop makes the bot reply with an album of images detailing what is currently in the fortnite shop
	elif (len(args) == 1 and args[0] == "shop"):
		bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text="Let me open the shop up! One second please.")
		bot.send_chat_action(chat_id=update.message.chat_id, action="UPLOAD_PHOTO")

		#Sends an album with every weekly item in the shop
		resp = fnite.getWeeklyStore()
		bot.send_media_group(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, media=resp)
		
		#Sends an album with every daily item in the shop
		resp = fnite.getDailyStore()
		bot.send_media_group(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, media=resp)

	#command /fortnite challenges makes the bot reply with the current weekly challenges in Fortnite
	elif (len(args) == 1 and args[0] == "challenges"):
		bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text="Let me check the challenges")
		resp = fnite.getChallenges()
		bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=resp)
	
	#command /fortnite [name] gets the bot to send [name]'s stats in the current Fortnite season
	else:
		name = ""
		for word in args:
			name = name + word + " "

		resp = fnite.getStats(name)
		bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=resp)

def apex(bot, update, args):
	msg_ID = update.message.message_id

	if not args:
		question = "@SaveTheBeeees @anobdya @hotterthanahotdog @AtraWolf @bleachonmytshirt @prankpatrol apex?"
		bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)
	else:
		platform = args[0]
		player_name = ""
		for i in args[1:]:
				player_name = player_name + i + " "


		if(platform.lower() == 'xbox'):
			platform = 1
		elif(platform.lower() == 'psn' or platform.lower() == 'ps4'):
			platform = 2
		elif(platform.lower() == 'pc'):
			platform = 5
		else:
			bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text="Type /apex [platform] [name]\nPlatforms are xbox, psn, pc")
	
	resp = apx.getStats(platform, player_name)
	bot.send_message(parse_mode='MARKDOWN', chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=resp)
		

#command /overwatch makes the bot tag everyone in the chat that plays Overwatch by their telegram username
def overwatch(bot, update):		
	msg_ID = update.message.message_id
	question = "@SaveTheBeeees @anobdya @hotterthanahotdog @bleachonmytshirt @prankpatrol @AtraWolf Overwatch?"
	bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)

#command /valorant makes the bot tag everyone in the chat that plays Overwatch by their telegram username
def valorant(bot, update):		
	msg_ID = update.message.message_id
	question = "@SaveTheBeeees @anobdya @hotterthanahotdog @bleachonmytshirt @prankpatrol @AtraWolf @GangplankWinsIfHeDoesntAFK Valorant?"
	bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)
		
#command /forest makes the bot tag everyone in the chat that plays The Forest by their telegram username
def forest(bot, update):
	msg_ID = update.message.message_id
	question = "@prankpatrol @Insolent_child @AtraWolf @SaveTheBeeees @anobdya forest?"
	bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)

#command /dauntless makes the bot tag everyone in the chat that plays Dauntless by their telegram username
def dauntless(bot, update):
	msg_ID = update.message.message_id
	question = "@prankpatrol @Insolent_child @AtraWolf @SaveTheBeeees @anobdya dauntless?"
	bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=question)

#Method that reads every message sent in chat, and if a user says certain words it will interrupt.
def interjection(bot, update):
	#get some info for each message, like who sent it
	from_user = update.message.from_user.first_name
	msg_ID = update.message.message_id
	msg_text = update.message.text.lower()
	msg_lst = msg_text.split()

	#If Kalada says the word yi, then trash talk him (replies are picked at random from a list in strings.py)
	if(from_user == "Kalada" and "yi" in msg_lst):
		i = random.randrange(len(strings.master_yi))
		reply = strings.master_yi[i]
		bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=msg_ID, text=reply)

#If a user types in a command that doesn't exist then the bot will reply to them (doesn't work yet)
def unknown(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Sorry I didn't understand that command. :(")

#command /caps [string] makes the bot reply with the same string but in all upper case
def caps(bot, update, args):
	text_caps = ' '.join(args).upper()
	bot.send_message(chat_id=update.message.chat_id, text=text_caps)

#Main method that is ran when the bot is started up
def main():
	#Basic stuff required by telegram to make the bot work. Basically lets Telegram know who the bot is / who it belongs to.
	bot = telegram.Bot(token=TOKEN)
	updater = Updater(token=TOKEN)
	dispatcher = updater.dispatcher
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

	#Each command that the bot can handle needs a "Handler". These basically map the command (/[command] to a method in main.py)
	#It is set up so the commands execute methods with the exact same name, but the command is the first argument, and the method that it executes is the second.
	#pass_args says whether the command can take additional arguments (bot uses these for summoner names, or fortnite names). Default is to False
	start_handler = CommandHandler('start', start)
	help_handler = CommandHandler('help', help)
	caps_handler = CommandHandler('caps', caps, pass_args=True)
	stats_handler = CommandHandler('stats', stats, pass_args=True)
	match_handler = CommandHandler('match', match, pass_args=True)
	league_handler = CommandHandler('league', league, pass_args=True)
	dota_handler = CommandHandler('dota', dota)
	fortnite_handler = CommandHandler('fortnite', fortnite, pass_args=True)
	apex_handler = CommandHandler('apex', apex, pass_args=True)
	overwatch_handler = CommandHandler('overwatch', overwatch)
	valorant_handler = CommandHandler('valorant', valorant)
	forest_handler = CommandHandler('forest', forest)
	dauntless_handler = CommandHandler('dauntless', dauntless)
	ror_handler = CommandHandler('ror', ror)
	r6s_handler = CommandHandler('r6', r6)
	interjection_handler = MessageHandler(Filters.all, interjection)

	#Unkown doesn't quite work yet
	unknown_handler = MessageHandler(Filters.command, unknown)

	#This adds handlers to the bot's dispatcher more info at: https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.dispatcher.html
	#Basically every command needs to have a handler and then that handler needs to be added to the dispatcher to work. If you don't add a handler to the dispatcher then it won't work.
	dispatcher.add_handler(start_handler)
	dispatcher.add_handler(help_handler)
	dispatcher.add_handler(caps_handler)
	dispatcher.add_handler(stats_handler)
	dispatcher.add_handler(match_handler)
	dispatcher.add_handler(league_handler)
	dispatcher.add_handler(dota_handler)
	dispatcher.add_handler(fortnite_handler)
	dispatcher.add_handler(apex_handler)
	dispatcher.add_handler(overwatch_handler)
	dispatcher.add_handler(valorant_handler)
	dispatcher.add_handler(forest_handler)
	dispatcher.add_handler(dauntless_handler)
	dispatcher.add_handler(ror_handler)
	dispatcher.add_handler(r6s_handler)

	dispatcher.add_handler(interjection_handler)	
	dispatcher.add_handler(unknown_handler)

	#After setting up the handlers and the dispatcher, the bot starts polling, which means that the bot will now read updates from Telegram, and any update will be handled by a handler
	#Because of this, the program runs until forcefully quit (^C)
	updater.start_polling()

main()
