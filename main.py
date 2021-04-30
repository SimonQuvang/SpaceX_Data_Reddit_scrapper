#######
# IMPORT PACKAGES
#######

# Twitter APIs keys
# Ksjc8l6Twa2FngctK7mXRJZTw
# Twitter API key secret
# fgO0Cji6HQvm4fONlfdDtcngvjtEwupLpqg6Uu22qwfp7yt7cN
# Acess token 551739406-R145ECVVtt8aG363GG77P8Tpp1emsyJ9n918T0iD
# Acess token secret mgR5Iy1r4J28DyTEIhab1ReNU3juwj67FvELq3jEArgjg

import csv
import re

import pandas as pd
import praw
import tweepy

def find_url(string):
    # Source for code https://www.geeksforgeeks.org/python-check-url-string/
    # findall() has been used
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+" \
            r"\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]


def find_date(string):
    regex = r"[\d]{4}-[\d]{2}-[\d]{2}"
    date = re.findall(regex, string)
    return date


def find_comment(string):
    regex = r'\[.*?\]'
    comments = re.finditer(regex, string)
    return [x[0] for x in comments]


def find_starship(string):
    regex = r'\*\*.*?\*\*'
    star = re.findall(regex, string)
    return star


# Acessing the reddit api


reddit = praw.Reddit(client_id="8Nx0ziWscx4hLg",  # my client id
                     client_secret="tNGXrHTHLh2ezy7DqJcZQ4mAjfdsaw",  # your client secret
                     user_agent="my user agent")  # user agent name

subreddit = reddit.subreddit('SpaceX')  # Chosing the subreddit

########################################
#   CREATING DICTIONARY TO STORE THE DATA WHICH WILL BE CONVERTED TO A DATAFRAME
########################################

#   NOTE: ALL THE POST DATA AND COMMENT DATA WILL BE SAVED IN TWO DIFFERENT
#   DATASETS AND LATER CAN BE MAPPED USING IDS OF POSTS/COMMENTS AS WE WILL
#   BE CAPTURING ALL IDS THAT COME IN OUR WAY

# SCRAPING CAN BE DONE VIA VARIOUS STRATEGIES {HOT,TOP,etc} we will go with keyword strategy i.e using search a keyword
submissions = []

def get_dev_post(x):
    starship = subreddit.search(f'starship_development_thread #{x}', limit=1)
    submissions.append(starship.__next__())


for x in range(3,21):
    get_dev_post(x)

for submission in submissions:
    print(submission)
post_dict = {
    "selftext": []
}

for submission in submissions:
    post_dict["selftext"].append(submission.selftext)

post_data = pd.DataFrame(post_dict)
post_data.to_csv("subreddit.csv", index=False)

update_dict = {}

with open('subreddit.csv', 'r+') as file:
    reader = csv.reader(file, delimiter="\n")
    save_text = False
    prev_line = ""
    starship_name = ""
    update = pd.DataFrame()
    for each_row in reader:
        if save_text:
            if not each_row:
                save_text = False
            else:
                line = each_row[0].encode('ascii', 'ignore').decode()
                url = (find_url(line))
                date = str(find_date(line))
                comments = find_comment(line)
                date = re.sub(r'\**|\[|\]', "", date)
                for i in range(0, len(url)):
                    comment = re.sub(r'\**|\[|\]', "", str(comments[i]))
                    dict = {"starship": starship_name, "date": date, "comment": comment, "url": str(url[i])}
                    update = update.append(dict, ignore_index=True)
        if "| :--- | :--- |" in str(each_row):
            save_text = True
            starship_name = find_starship(prev_line[0])
            starship_name = re.sub(r'\**|\[|\]', "", str(starship_name))
            print(starship_name)
        prev_line = each_row  # Saving the prev line to be used to get the table name later on
    update.to_csv("subreddit1.csv")
