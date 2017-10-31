#!/usr/bin/python
# LinkRav_Bot
# by /u/bananagranola
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
#TODO: Fix
#def delete_downvotes (user):
#        user_comments = user.get_comments(limit = 20)
#        for user_comment in user_comments:
#                score = user_comment.score
#                if score < karma_floor:
#                        user_comment.delete()
#                        logger.debug("DELETING: %s", user_comment.id)

def uniq (input):
        output = []
        for x in input:
                if x not in output:
                        output.append(x)
        return output

# process comments
def process_comment (ravelry, comment):
        comment_reply = ""
        
        # ignore comments that didn't call LinkRav
        # TODO: Replace RavBot with LinkRav
        if re.search('.*RavBot.*', comment.body, re.IGNORECASE):
                matches = re.findall(RAV_MATCH, comment.body, re.IGNORECASE)
        else:
                #TODO: Fix this
                #logger.debug("COMMENT IGNORED: %s", comment.permalink)
                return ""

        # iterate through comments that did call LinkRav
        if matches is not None:
                #TODO: Fix this
                #logger.debug("COMMENT PERMALINK: %s", comment.permalink)

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
                reddit = praw.Reddit('bot1', user_agent = 'linkrav by /u/bananagranola')

                # retrieve comments
                # TODO: Insert limit here
                inbox = reddit.inbox.unread(True, limit=None)

                # iterate through comments
                for item in inbox:

                        #Check if comment
                        if isinstance(item, Comment):
                                
                                # process comment and submit
                                comment_reply = process_comment (ravelry, item)
                                                                         
                                reply = None
                                if comment_reply != "":
                                        reply = item.reply(comment_reply)
                                        #TODO: Fix this line
                                        #logger.info(reply.permalink)
                        else:
                                continue

                #TODO: Reenable when fixed
                #delete_downvotes(reddit.redditor(reddit_username))

        except requests.exceptions.ConnectionError, e:
                logger.error('ConnectionError: %s', str(e.args))
                sys.exit(1)
        except requests.exceptions.HTTPError, e:
                logger.error('HTTPError: %s', str(e.args))
                sys.exit(1)
        except requests.exceptions.Timeout, e:
                logger.error('Timeout: %s', str(e.args))
                sys.exit(1)
#TODO: Fix praw exceptions
#        except praw.errors.ClientException, e:
#                logger.error('ClientException: %s', str(e.args))
#                sys.exit(1)
#        except praw.errors.ExceptionList, e:
#                logger.error('ExceptionList: %s', str(e.args))
#                sys.exit(1)
#        except praw.errors.APIException, e:
#                logger.error('APIException: %s', str(e.args))
#                sys.exit(1)

if __name__ == "__main__":
        main()

