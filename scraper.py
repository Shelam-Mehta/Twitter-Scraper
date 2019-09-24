from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import re
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options
import sys

def TopHashtag(city,country):
    url='https://trends24.in/'+country+'/'+city+'/'
    r=requests.get(url)
    text=r.text
    soup=BeautifulSoup(text,'html.parser')
    ol=soup.find_all('ol',{'class':"trend-card__list"})
    top_tag=re.findall(r'(?<=<a href=")[^"]*',str(ol[-1]))
    return top_tag
def HeadlessMode():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=options)
    return browser

def ScrollPage(browser):
    SCROLL_PAUSE_TIME = 1
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    return browser
def OpenTwitter(tag):
    hashtagurl=tag
    browser.get(hashtagurl+'%20near%3A"'+city+'"%20within%3A50mi&src=typd')
    return browser
def ScrapeTwitterUrl(browser,url):
    soup=BeautifulSoup(browser.page_source,'html.parser')
    tags=soup.find_all('p',attrs={'class':"TweetTextSize js-tweet-text tweet-text"})
    comments=soup.find_all('span',attrs={'class':"ProfileTweet-actionCountForPresentation"})
    timestamp=soup.find_all('a',attrs={'class':"tweet-timestamp js-permalink js-nav js-tooltip"})
    return tags,comments,timestamp

def DeleteDuplicateComments(comments):
    response=[]
    length=len(comments)
    for i in range(length,-1,-1):
        if(i%5==2 or i%5==4):
            comments.pop(i)
    for i in range(len(comments)):
        if(comments[i].text==""):
            response+=[0]
        elif('K' in comments[i].text):
            response+=[float(re.findall('[0-9.]+',comments[i].text)[0])*1000]
        elif('M' in comments[i].text):
            response+=[float(re.findall('[0-9.]+',comments[i].text)[0])*1000000]
        else:
            response+=[float(comments[i].text)]
    return response         
            
def GetUserInfo(timestamp):
    userid=[]
    tweetid=[]
    time=[]
    tweet=[]
    for i in range(len(timestamp)):
        l=timestamp[i]["href"].split('/')
        userid+=[l[1]]
        tweetid+=[l[3]]
    for i in range(len(timestamp)):
        time+=[timestamp[i]["title"]]
    for i in range(len(tags)):
        tweet+=[tags[i].text]
    
    return userid,tweetid,time,tweet
    
def SeperateComments(response):
    comment=[]
    like=[]
    retweet=[]
    for i in range(len(response)):
        if(i%3==0):
            comment+=[response[i]]
        elif(i%3==1):
            retweet+=[response[i]]
        else:
            like+=[response[i]]
    return comment,like,retweet

def CreateDataFrame(tweet,userid,comment,like,retweet,time,city):
    df=pd.DataFrame(tweet)     
    df.columns=["tweet"]

    df['tweetid']=tweetid
    df['userid']=userid
    df['comment']=comment
    df['like']=like
    df['retweet']=retweet
    df['Time']=time
    df["score"]=df.retweet*3+df.comment*2+df.like
    df['city']=city
    return df
    
