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
from optparse import OptionParser
from praw.models import Comment
# import linkrav_bot modules
from auth_my import *
from constants import *
from settings import *
from ravelry import *
from pattern import *
from project import *
from yarn import *

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

# process comments
def process_comment_subreddit (ravelry, comment):
    comment_reply = ""
        
    matches = re.findall(RAV_MATCH, comment.body, re.IGNORECASE)

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

def process_comment_inbox (ravelry, comment):
    comment_reply = ""
        
    # ignore comments that didn't call LinkRav
    if re.search('.*RavBot.*', comment.body, re.IGNORECASE):
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

def CheckComments(item, reddit):
    Continue = False

    comment = reddit.comment(item.id)
    comment.refresh()
    comment.replies.replace_more(0)

    for com in comment.replies:
        if com.author == "RavBot":
            Continue = True
            break

    return Continue

def CheckInbox(reddit, ravelry):
    logger.info("Checking inbox...")

    # retrieve comments
    inbox = reddit.inbox.unread(True, limit=25)

    # iterate through comments
    for item in inbox:

        #Check if comment
        if isinstance(item, Comment):

            if CheckComments(item, reddit):
                logger.info("Comment " + item.id + " ignored: Already replied")
                continue
                                                
            # process comment and submit
            comment_reply = process_comment_inbox(ravelry, item)
                                                                         
            reply = None
            if comment_reply != "":
                reply = item.reply(comment_reply)
                logger.info(item.id)
            else:
                logger.debug("Parse failed")
        else:
            continue


    delete_downvotes(reddit.redditor('RavBot'))
                

def CheckSub(reddit, ravelry):
    logger.info("Checking subbredits....")

    for item in reddit.subreddit("knitting+crochet").comments(limit=250):
        if item.author == "RavBot":
            logger.debug("RavBot comment. Ignorning comment " + item.id)
            continue
        matches = re.findall(RAV_MATCH, item.body, re.IGNORECASE)

        if len(matches) == 0:
            logger.debug("No link. Ignorning comment " + item.id)
            continue

        if CheckComments(item, reddit):
            logger.info("Comment " + item.id + " ignored: Already replied")
            continue

        comment_reply = process_comment_subreddit (ravelry, item)
                                                                         
        reply = None
        if comment_reply != "":
            reply = item.reply(comment_reply)
            logger.info(item.id)
        else:
            logger.debug("Parse failed")


def main():
    parser = OptionParser()
    parser.add_option("-i", "--inbox", action="store_true", dest="inbox")
    parser.add_option("-s", "--subreddit", action="store_true", dest="subreddit")
    (options, args) = parser.parse_args()

    if len(sys.argv) == 1:
        logger.debug("Must specify atleast 1 runmode")

    try:
        # log into ravelry
        ravelry = Ravelry(ravelry_accesskey, ravelry_personalkey)

        # log in to reddit
        reddit = praw.Reddit('LinkRav', user_agent = 'linkrav by /u/bananagranola')

        if options.inbox == True:
            CheckInbox(reddit, ravelry)
        if options.subreddit == True:
            CheckSub(reddit, ravelry)
    
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