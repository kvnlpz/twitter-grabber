from twython import Twython
from twython import TwythonStreamer
from github import Github
from github import InputGitTreeElement
from datetime import date
import os
import sys
import time
import yaml

conf = yaml.load(open('twitterAPI.yml'))

TWITTER_APP_KEY = conf['twitter']['twitterAppKey']
TWITTER_APP_KEY_SECRET = conf['twitter']['twitterAppKeySecret']
TWITTER_ACCESS_TOKEN = conf['twitter']['twitterAccessToken']
TWITTER_ACCESS_TOKEN_SECRET = conf['twitter']['twitterAccessTokenSecret']
token = conf['github']['token']


g = Github(token)


def create_file_and_send(post_url, post_author):
    count = 0
    
    # YY-mm-dd
    todays_date = date.today()
    
    t = time.localtime()
    
    # current_time = time.strftime("%H:%M:%S", t)
    
    current_time = int(time.time())
    
    file_title = "" + str(todays_date) + "-twitter-" + str(current_time) + ".markdown"
    
    string_to_write = "--- \nlayout: post \ntitle: " + "Tweet by @" + post_author + " \ndate: " + str(todays_date) + " " + str(current_time) + " \ncategories: twitter \n--- "
    
    string_to_write = string_to_write + "\n" + post_url
    
    user = g.get_user()
    
    repo = g.get_repo('kvnlpz/RSSFeed')  # repo name
    print("get_labels")
    labels = repo.get_labels()
    
    repo.create_file("_posts/" + file_title, "twitter update", string_to_write, branch="main")





client = Twython(TWITTER_APP_KEY, TWITTER_APP_KEY_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

twitter_names_file = open("twitter_names.txt", "r")

twitter_names_list = twitter_names_file.readlines()

twitter_names_file.close()

twitter_track = ",".join(twitter_names_list).replace("\n", "")

# print(twitter_track)

# look up each user and get their respective IDs
ID_list_lookup = client.lookup_user(screen_name=twitter_track)

ID_list = []

# Loop through the results (Twitter screen names)

for user in ID_list_lookup:
    # print(user["id_str"])
    ID_list.append(str(user["id_str"]))


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            universal_post_url = "https://twitter.com/o/status/" + str(data['id_str'])

            # print(universal_post_url)

            # passing in the user tweet URL and screen name of the user
            try:
                create_file_and_send(universal_post_url, data['user']['screen_name'])
                time.sleep(3)
            except:
                print("An exception occurred")
                time.sleep(50)


    def on_error(self, status_code, data):
        print(status_code)



stream = MyStreamer(TWITTER_APP_KEY, TWITTER_APP_KEY_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

# stream.statuses.filter(track=twitter_track)

stream.statuses.filter(follow=ID_list)



