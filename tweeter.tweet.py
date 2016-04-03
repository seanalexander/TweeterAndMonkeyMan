#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, time, sys

from Adafruit_BME280 import *#https://learn.adafruit.com/adafruit-bme280-humidity-barometric-pressure-temperature-sensor-breakout/wiring-and-test
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
  while True:
    sensor = BME280(mode=BME280_OSAMPLE_8)
    degrees = sensor.read_temperature()
    pascals = sensor.read_pressure()
    hectopascals = pascals / 100
    humidity = sensor.read_humidity()

    #TweetTemperatureString = 'Timestamp = {0:0.3f}, Temp = {1:0.3f} deg C, Pressure = {2:0.2f} hPa, Humidity = {3:0.2f} %'.format(sensor.t_fine, degrees, hectopascals, humidity)
    DateTweeted = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    TweetTemperatureString = 'Date = {0}, Temp = {1:0.3f} deg C, Pressure = {2:0.2f} hPa, Humidity = {3:0.2f} %'.format(DateTweeted, degrees, hectopascals, humidity)


    print "Writing Tweet {} @ {} \n\tTweet: {}".format(TweetsThisRun, DateTweeted, TweetTemperatureString)
    api.update_status(TweetTemperatureString)
    TweetsThisRun += 1
    time.sleep(900)
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
  print "Exiting."
