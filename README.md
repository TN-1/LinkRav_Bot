LinkRav_Bot
===========
To install:  
`pip install -r requirements.txt`  
Create ravelry API account, and add access credentials to auth.py  
`cp auth.py auth_my.py`  
Create reddit API account, and add credentials to praw.ini    
Run with:  
`python LinkRav_Bot.py [-i -s]`  
-i flag to only check for comments that explicetly call RavBot, -s to check subbredit for any comment with a ravelry link. Can be run together.  