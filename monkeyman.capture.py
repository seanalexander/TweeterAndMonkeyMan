#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time, sys, sqlite3
#from Adafruit_BME280 import *
from datetime import datetime

#argfile = str(sys.argv[1])

#enter the corresponding information from your Twitter application:
CONSUMER_KEY = 'SUPERSECRETKEYLOL'#keep the quotes, replace this with your consumer key
CONSUMER_SECRET = 'SUPERSECRETKEYLOL'#keep the quotes, replace this with your consumer secret key
ACCESS_KEY = 'SUPERSECRETKEYLOL'#keep the quotes, replace this with your access token
ACCESS_SECRET = 'SUPERSECRETKEYLOL'#keep the quotes, replace this with your access token secret
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

TweetsThisRun = 1;
try:
  #sensor = BME280(mode=BME280_OSAMPLE_8)
  #degrees = sensor.read_temperature()
  #pascals = sensor.read_pressure()
  #hectopascals = pascals / 100
  #humidity = sensor.read_humidity()

  conn = sqlite3.connect('/home/pi/FTP/DataCollect/tweeter/TweeterMonkeyWeatherMan.db')
  queryString_Select = "SELECT ID, CAPTURED, DEGREES, HECTOPASCALS, HUMIDITY, ISTWEETED from WeatherLog ORDER BY ID DESC LIMIT 1"
  print "Opened database successfully";

  IsTweeted = 0
  cursor = conn.execute(queryString_Select)
  for row in cursor:
     #print "ID = ", row[0]
     print "Captured = ", row[1]
     print "DEGREES = ", row[2]
     print "HECTOPASCALS = ", row[3]
     print "HUMIDITY = ", row[4]
     print "ISTWEETED = ", row[5], "\n"
     WeatherLog_ID = int(row[0])
     DateTweeted = row[1]
     degrees = float(row[2])
     hectopascals = float(row[3])
     humidity = float(row[4])
     istweeted = int(row[5])

  conn.close()

  TweetTemperatureString = 'Date = {0},\n Temp = {1:0.3f} deg C,\n Pressure = {2:0.2f} hPa,\n Humidity = {3:0.2f} %'.format(DateTweeted, degrees, hectopascals, humidity)

  TweetSuccess = 0
  print ("WeatherLog_ID: {} IsTweeted: {}").format(WeatherLog_ID, IsTweeted)
  if WeatherLog_ID > 0 and IsTweeted < 1:
    try:
      print "Writing Tweet {} @ {} \n\tTweet: {}".format(TweetsThisRun, DateTweeted, TweetTemperatureString)
      api.update_status(TweetTemperatureString)
      TweetSuccess = 1
      print "TweetSuccess: {}".format(TweetSuccess)
    except:
      TweetSuccess = 0
  else:
    print "Results were blank or last record was already tweeted."

    if TweetSuccess > 0:
      conn = sqlite3.connect('/home/pi/FTP/DataCollect/tweeter/TweeterMonkeyWeatherMan.db')
      print "Opened database successfully";
      queryString_Update = "UPDATE WeatherLog SET ISTWEETED = 1 WHERE ID = {0}".format(WeatherLog_ID)
      print "queryString_Update: {}".format(queryString_Update)
      #conn.execute(queryString_Update)
      conn.commit()
      conn.close()
      print "Closed database successfully";
      TweetsThisRun += 1
    else:
      print "Was not able to Tweet"

  #print "Sleeping for {} seconds".format("60")
  #time.sleep(60)

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
  print "Exiting."
