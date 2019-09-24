import sys

    
if(__name__=="__main__"):
  for i in range(1,len(sys.args)):
      cities+=[sys.args[i]]
#  'Bhopal', 'Jabalpur', 'Ujjain','Gwalior','Sagar','Khajuraho','Shivpuri','Satna',
# 'Rewa','Ratlam','Mandav','Pachmarhi','Burhanpur','Orchha','Dewas','Sanchi','Katni','Bhedaghat',
# 'Chhindwara','Neemuch','Vidisha','Mandsaur','Bhind','Maheshwar','Khandwa','Chitrakoot','Chhatarpur',
# 'Gwalior','Khargone','Morena','Singrauli','Hoshangabad'

  country="india"
  
  columnname=['tweet','tweetid','userid','comment','like','retweet','Time','score','city']

  df=pd.DataFrame(columns=columnname)
    
  for city in cities:
    tag=TopHashtag(city,country)
    browser=HeadlessMode()
    for i in range(len(tag)):
        url=tag[i]
        browser=OpenTwitter(url)
        browser=ScrollPage(browser)
        tags,comments,timestamp=ScrapeTwitterUrl(browser,url)
        userid,tweetid,Time,tweet=GetUserInfo(timestamp)
        comments=DeleteDuplicateComments(comments)
        comment,like,retweet=SeperateComments(comments)
        if(len(comment)!=0):  
            newdf=CreateDataFrame(tweet,userid,comment,like,retweet,Time,city)
            df=df.append(newdf)
            df=df.drop_duplicates()   
df.to_csv("twitter_data.csv")
