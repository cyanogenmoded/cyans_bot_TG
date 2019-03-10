
from uuid import uuid4
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler as CH ,InlineQueryHandler
from random import randint
import logging
from googleapiclient.discovery import build
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
updater = Updater(token='<token>')
dispatcher = updater.dispatcher
results=[]


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)


def aut(bot, update, args):
    A=""
    for Z in args:
        j = len(Z)
        for x in range(0, j):
            Y=randint(0, 1)
            if Y==0:
                A +=Z[x].lower()
            else:
                A +=Z[x].upper()
        A += " "
    bot.send_message(chat_id=update.message.chat_id, text=A)


auts_handler = CH('auts', aut, pass_args=True)
dispatcher.add_handler(auts_handler)
auts_handler = CH('aut', aut, pass_args=True)
dispatcher.add_handler(auts_handler)
caps_handler = CH('caps', caps, pass_args=True)
dispatcher.add_handler(caps_handler)
start_handler = CH('start', start)
dispatcher.add_handler(start_handler)

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def youtube_search(a, s):
    A=""
    B=""
    C=""
    print(a)
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey='AIzaSyDlS4v1o_LqdYDD_nEAXrgBlQXq4EbSXDw')
    search_response = youtube.search().list(q=a, part='id,snippet', maxResults=s).execute()
    # Call the search.list method to retrieve results matching the specified
    # query term.
    videos = []
    channels = []
    playlists = []
    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.

    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append('[%s](www.youtube.com/watch?v=%s)' % (search_result['snippet']['title'], search_result['id']['videoId']))
            if s==20:
                global results
                results.append(
                    InlineQueryResultArticle(
                    id=uuid4(),
                    title=search_result['snippet']['title'],
                    url="www.youtube.com/watch?v=%s" %search_result['id']['videoId'],
                    input_message_content= InputTextMessageContent("www.youtube.com/watch?v=%s" %search_result['id']['videoId']),
                    thumb_url="https://img.youtube.com/vi/%s/default.jpg" %search_result['id']['videoId'],
                    description= "%s" %search_result['snippet']['description'],
                    )
                )
        elif search_result['id']['kind'] == 'youtube#channel':
            channels.append('[%s](www.youtube.com/channel/%s)' % (search_result['snippet']['title'], search_result['id']['channelId']))
        elif search_result['id']['kind'] == 'youtube#playlist':
            playlists.append('%s (%s)' % (search_result['snippet']['title'], search_result['id']['playlistId']))
    for i in range(len(videos)):
        A+=videos[i]+"\n\n"
    if channels:
        for i in range(len(channels)):
            B+=channels[i]+"\n\n"
    if playlists:
        for i in range(len(playlists)):
            C+=playlists[i]+"\n\n"
    return A, B, C


def ytb(bot, update):
    T, T1, T2= youtube_search(update.message.text[5:], 5)
    T= "Videos: \n"+T
    if T1:
        T+="\nChannels: \n"+T1
    if T2:
        T+="\nPlaylists: \n"+T2
    bot.send_message(chat_id=update.message.chat_id, text=T, parse_mode='Markdown')


def inline(bot, update):
    query =update.inline_query.query
    youtube_search(query, 20)
    update.inline_query.answer(results)
    results.clear()


ytb_handler = CH('ytb', ytb)
dispatcher.add_handler(ytb_handler)
dispatcher.add_handler(InlineQueryHandler(inline))
updater.start_polling()


