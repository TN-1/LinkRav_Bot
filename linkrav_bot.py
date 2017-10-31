#!/usr/bin/python
# LinkRav_Bot
# by /u/bananagranola
# Upgraded to Praw 5 by /u/randomstonerfromaus
# posts ravelry information on settings.bot_subreddit
# main()

# import libs
import logging
import praw
import re
import requests
import signal
import sys

# import linkrav_bot modules
from auth_my import *
from constants import *
from settings import *
from ravelry import *
from pattern import *
from project import *
from yarn import *

from praw.models import Comment

# basic logging
logging.basicConfig()
logger = logging.getLogger('linkrav_bot')
logger.setLevel(logging.DEBUG)
        
# ctrl-c handling
def signal_handler(signal, frame):
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# delete comments with lots of downvotes
def delete_downvotes (user):
        user_comments = user.comments.new(limit = 20)
        for user_comment in user_comments:
                score = user_comment.score
                if score < karma_floor:
                        user_comment.delete()
                        logger.debug("DELETING: %s", user_comment.id)

def uniq (input):
        output = []
        for x in input:
                if x not in output:
                        output.append(x)
        return output

def writeDB(m):
    s = ''
    for c in m:
        s = s + str(c) + '\n'
    x = open('database.txt','w')  
    x.write(s) 
    x.close() 

def readDB():
    x = open('database.txt', 'r') 
    s = x.read()
    c = s.split()
    x.close()
    return c

# process comments
def process_comment (ravelry, comment):
        comment_reply = ""
        
        # ignore comments that didn't call LinkRav
        if re.search('.*LinkRav.*', comment.body, re.IGNORECASE):
                matches = re.findall(RAV_MATCH, comment.body, re.IGNORECASE)
        else:
                logger.debug("COMMENT IGNORED: %s", comment.id)
                return ""

        # iterate through comments that did call LinkRav
        if matches is not None:
                logger.debug("COMMENT ID: %s", comment.id)

                matches = uniq(matches)
                
                # append to comments
                for match in matches:
                        match_string = ravelry.url_to_string (match)
                        if match_string is not None:
                                comment_reply += match_string
                                comment_reply += "*****\n"

        # generate comment
        if comment_reply != "":
                comment_reply = START_NOTE + comment_reply + END_NOTE
                logger.debug("\n\n-----%s-----\n\n", comment_reply)

        # return comment text
        return comment_reply

def main():

        try:
                # log into ravelry
                ravelry = Ravelry(ravelry_accesskey, ravelry_personalkey)

                # log in to reddit
                reddit = praw.Reddit('LinkRav', user_agent = 'linkrav by /u/bananagranola')

                finishedComments = readDB()
                
                # retrieve comments
                inbox = reddit.inbox.unread(True, limit=100)

                # iterate through comments
                for item in inbox:

                        #Check if comment
                        if isinstance(item, Comment):

                                if item.id in finishedComments:
                                        #This will spam the log, but probably a good idea to leave for debug purposes.
                                        logger.debug("COMMENT IGNORED: %s", item.id)
                                        continue
                                
                                # process comment and submit
                                comment_reply = process_comment (ravelry, item)
                                                                         
                                reply = None
                                if comment_reply != "":
                                        reply = item.reply(comment_reply)
                                        logger.info(item.id)
                                finishedComments.append(item.id)
                        else:
                                continue

                #TODO: Reenable when fixed
                delete_downvotes(reddit.redditor('LinkRav_Bot'))

                writeDB(finishedComments)
                
        except requests.exceptions.ConnectionError, e:
                logger.error('ConnectionError: %s', str(e.args))
                sys.exit(1)
        except requests.exceptions.HTTPError, e:
                logger.error('HTTPError: %s', str(e.args))
                sys.exit(1)
        except requests.exceptions.Timeout, e:
                logger.error('Timeout: %s', str(e.args))
                sys.exit(1)
        except praw.exceptions.ClientException, e:
                logger.error('ClientException: %s', str(e.args))
                sys.exit(1)
        except praw.exceptions.PRAWException, e:
                logger.error('ExceptionList: %s', str(e.args))
                sys.exit(1)
        except praw.exceptions.APIException, e:
                logger.error('APIException: %s', str(e.args))
                sys.exit(1)

if __name__ == "__main__":
        main()

