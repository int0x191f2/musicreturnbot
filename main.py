from telegram import Updater
import telegram
import logging
import os

logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot,update):
	bot.sendMessage(update.message.chat_id,text="testText")

def error(bot,update,error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def returnMusic(bot, update):
	u=update
	id = (u.message.chat_id)
	update_id = (u.update_id)
	last_id=update_id
	try:
		cleanVideo()
		title=os.popen("./youtube-dl -e "+u.message.text).read()
		open("current_title",'w').write(str(title))
		title=os.popen("cat current_title | tr -dc '[:alnum:]'").read()
		bot.sendMessage(id,"Downloading video: "+title)
		downloadVideo(u.message.text)
		bot.sendMessage(id,"Converting video: "+title)
		convertVideo()
		renameVideo(title)
		bot.sendChatAction(chat_id=id, action=telegram.ChatAction.UPLOAD_AUDIO)
		bot.sendAudio(id,open(title+".mp3","r"))
		cleanVideo()
	except Exception, e:
		bot.sendMessage(id,"there was a problem")
		bot.sendMessage(id,str(e))
		cleanVideo()
		print("There was a problem")
		print("ID:"+str(last_id))
		open("update_id",'w').write(str(last_id))

def downloadVideo(url):
	command="./youtube-dl -o tmpa "+url
	print(command)
	os.system(command)

def convertVideo():
	command="ffmpeg -i tmpa.* a.mp3"
	print(command)
	os.system(command)

def renameVideo(title):
	command="mv a.mp3 "+title+".mp3"
	print(command)
	os.system(command)

def cleanVideo():
	command="rm *.mp3 tmpa.* tmp.*"
	os.system(command)

def main():
	updater=Updater("136820376:AAFgZ66FHblXImb0m-QyHj5i4gZAQ-5sN_c")
	dp=updater.dispatcher
	dp.addTelegramCommandHandler("start", start)

	dp.addTelegramMessageHandler(returnMusic)

	dp.addErrorHandler(error)

	updater.start_polling()

	updater.idle()

if __name__ == '__main__':
	main()
