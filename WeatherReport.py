#! /usr/bin/python
# coding = utf-8

#Function: get weather information from weather.com.cn
#by hunter
#2016/03/29

import os
import urllib.request
import sys
import json
import time

#get token
def get_token():
    api_key="qlZ82V3EaOZ6nz49gusePtNR"
    sec_key="3e00c74f7fcbb4f1e2e5b5f2f35744a3"
    auth_url="https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id="+api_key+"&client_secret="+sec_key
    
    res = urllib.request.urlopen(auth_url)
    #print(res.read())
    json_data = res.read().decode('utf-8')
    #print(json_data)

    result = json.loads(json_data)['access_token']
    return result


def get_weather(city):
    api_key="c538cf4ff1a00633267ff4c15cb07d2b"
    weather_url="http://api.map.baidu.com/telematics/v3/weather?location="+city+"&output=json&ak="+api_key
    
    res = urllib.request.urlopen(weather_url)
    json_data = res.read().decode('utf-8')
    #print(json_data)
    json_data = json.loads(json_data)
    #get json data
    #check result status
    status = json_data['status']
    isTom = time.localtime().tm_hour>18
    index = 1 if isTom else 0
    initStr = '明天' if isTom else '今天'
    if status=='success':
        results=json_data['results'][0]
        pm25=results['pm25']
        weather_data=results['weather_data']
        date=weather_data[index]['date']
        weather=weather_data[index]['weather']
        wind=weather_data[index]['wind']
        temperature=weather_data[index]['temperature'].replace('~','到')
        if not isTom:
            return'{}是{} PM2.5是{} 天气{} {} 温度为{}'.format(initStr,date,pm25,weather,wind,temperature)
        else:
            return'{}是{} 天气{} {} 温度为{}'.format(initStr,date,weather,wind,temperature)
    else:
        return ''


token=get_token()
weather=get_weather('beijing')

if os.path.exists('/home/pi/weather/weather.txt'):
    with open('/home/pi/weather/weather.txt','wt') as f:
        f.write(weather)
        f.close()
        print(weather)
else:
    print('weather.txt not exists')
        

#tts
url='http://tsn.baidu.com/text2audio?tex='+weather+'&lan=zh&cuid=raspberrypi2&ctp=1&tok='+token

#print(url)
try:
    os.system('/usr/bin/mplayer "%s"' %(url))
except Exception as e:
    print('Exception',e)