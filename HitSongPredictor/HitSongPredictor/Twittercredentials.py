import tweepy

consumer_key = "tdFtNB2QVd7kbvOdEFNzfqJYr";
#eg: consumer_key = "YisfFjiodKtojtUvW4MSEcPm";


consumer_secret = "ibB8LicfiMMhPhEJhdnON4I2rou3SoAwgg7lcliMZxDqV6yKop";
#eg: consumer_secret = "YisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPm";

access_token = "496315468-Z2cO1GPvrb3BAGYdz94tBtQ55jPP8RcxCQkn9iti";
#eg: access_token = "YisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPm";

access_token_secret = "dpgwQ35BkBZBsJyU571C2WszJnDrxMrvWZ9AtyKiVU3jd";
#eg: access_token_secret = "YisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPm";


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)



