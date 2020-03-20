import tweepy
import textblob
from AppData import AppData
import json
from FacePlusPlusHelper import FacePlusPlus

# TwitteHelper class extracts all Twitter data. The output format and data collected can be adjusted in this class.

def getImageUrl(api, id):
    user = api.get_user(id)
    return (user.profile_image_url_https).replace("_normal", "")


def ScrapeTwitter():
    auth = tweepy.OAuthHandler(AppData.twitterconsumerkey, AppData.twitterconsumersecret)
    auth.set_access_token(AppData.twitteraccesstoken, AppData.twitteraccesssecret)

    api = tweepy.API(auth)

    search = tweepy.Cursor(api.search, q=AppData.keyword, count=200, geocode=AppData.location).pages(200)

    for page in search:
        for item in page:
            input = json.loads(json.dumps(item._json))
            text = input.get("text")
            time = input.get("created_at")
            tweetid = input.get("id_str")
            polarity = textblob.TextBlob(text).polarity
            subjectivity = textblob.TextBlob(text).subjectivity
            userid = input.get("user").get("id")
            demographcs = FacePlusPlus.getAttributes(getImageUrl(api, userid))
            gender = ""
            age = ""
            ethnicity = ""
            if (len(demographcs) > 0):
                gender = demographcs.get("gender").get("value")
                age = demographcs.get("age").get("value")
                ethnicity = demographcs.get("ethnicity").get("value")
            row = [tweetid, AppData.keyword, AppData.location, time, gender, age, ethnicity, polarity, subjectivity]
            print(row)
