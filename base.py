# -*- coding: utf-8 -*-
import praw
from sql import *
import datetime

from dotenv import load_dotenv
import os

reddit = praw.Reddit(
    client_id=os.getenv('client_id'),
    client_secret=os.gentenv('client_secret'),
    password=os.getenv('passwordd'),
    user_agent="Knickerless Asswipe 1.0",
    username="SergeantAngel_bot"
    )

bot_username = "SergeantAngel_bot"
subreddit = reddit.subreddit('hotfuzz+hotfuzzgifs')    #Making the code look prettier.


response = "-angrily slams £{} into the swear box-\n\nThank you, {}!\n\n^(\[Total donations:  £{}.  All proceeds go to the church roof\])"


def analysis(comment):
    wordList = {" nob ": .1, " nob": .1, "bastard": .2, "shit": .5, "fuck": 1, "cunt": 2}
    cost = 0.0
    for key in wordList.keys():
        if comment.count(key) > 0:
            cost = cost + (comment.count(key) * wordList[key])
    return cost


for comment in subreddit.stream.comments():
    timestamp = datetime.datetime.fromtimestamp(comment.created_utc)
    now = datetime.datetime.now()
    between = now - timestamp
    if between.days > 2:
        readComments = getComments()
        if comment.id in readComments:
            pass
        else:
            writeComment(comment.id)
    else:
        readComments = getComments()
        if comment.id in readComments or comment.author.name == bot_username:
            print("Skipping comment that was already in the database.\n\n")
            pass
        else:
            lower_body = comment.body.lower()
            url = "https://reddit.com{}".format(comment.permalink)
            charges = analysis(lower_body)
            if charges > 0.0:
                try:
                    writeCharges(comment.author.name,charges)
                    total = getCharges(comment.author.name)
                    commentText = response.format(charges,comment.author.name,round(total,1))
                    comment.reply(body=commentText)
                    comment.upvote()
                    writeComment(comment.id)
                except Exception as e:
                    messageToSend = "{} - {}".format(url,str(e))
                    reddit.redditor('THC-Lab__').message('Log', messageToSend)