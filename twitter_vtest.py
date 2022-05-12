# import the module
import tweepy

# assign the values accordingly
consumer_key = ""
consumer_secret = ""
access_token="37403074-nHSsKc9pjvNTtBluzf5vRyeZBHac4CS6999JJzCUW"
access_token_secret="llY0LMMNgwjUYUjlk5RcEaGwYcT7J6eqs10mMXwjQ6tKj"
bearer_token="AAAAAAAAAAAAAAAAAAAAAK6x%2BQAAAAAAtsXaFrZgMru8AecrCz11B3uiR3w%3DaiKx4Qvl7HirmcmFIQTvriCwglB00c5pg65FYJGylXZMTLqOkm"
api_key="a2KeLP9N8qfaC9b81DJta9dch"
api_secret_key="J7CEkv3SugAC3JEjvvu46gur4FNOXFiWhd8vzOmJNNkPINdwpk"
id_str_jitsu="37403074"
id_str_george="18240468"

# authorization of consumer key and consumer secret
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth = tweepy.OAuthHandler(api_key, api_secret_key)

# set access to user's access key and access secret
auth.set_access_token(access_token, access_token_secret)

# calling the api
api = tweepy.API(auth)

# using get_user with id
# _id = "103770785"
_id = id_str_george
user = api.get_user(user_id=_id)

# printing the name of the user
print("The id " + _id + " corresponds to the user with the name : " + user.name)

