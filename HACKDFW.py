import os
import sys
import requests
!pip install apify_client
from apify_client import ApifyClient
def main():
  client=ApifyClient("apify_api_VWOV6zDcQK07HdcleF0hQWuqe9pMTO2NjQiN")
  Eligible_influencers=0
  Participated_Influencers=0
  
  url="https://api.apify.com/v2/acts/apify~google-search-scraper/run-sync-get-dataset-items?token=apify_api_VWOV6zDcQK07HdcleF0hQWuqe9pMTO2NjQiN"

  accounts={"usernames": ["yeshwanth_kuchi","vsnikhil_10","raavibrahmateja","chandan_alwala","sahil_teja_","mtejovardhan",
                          "harshavardhan_choudhari","bitsaa_intl","pammentjimmy","surya_14kumar","jhulangoswami","psg",
                          "neymarjr","leomessi","achrafhakimi","kimpembe3","icc","espncricinfo"] }

  run = client.actor("zuzka/instagram-profile-scraper").call(run_input=accounts)
  # Fetch and print actor results from the run's dataset (if there are any)
  for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    c=0
    d=0
    common=0
    for key in item.keys():
      if key=='followersCount' and item['followersCount']>1000 and item['private']=="False" and item['hasChannel']=="True":
        c+=1
      if key=="hashtags" and item[key] and not str(item['username'])+"#with_chester_cheetah" in item[key] and item['hasChannel']=="True" and item['private']=="False":
        c+=1
      elif key=="hashtags" and item[key] and str(item['username'])+"#with_chester_cheetah" in item[key] and item['private']=="False":
          common+=1
      elif key=="hashtags" and not item[key] and item['private']=="False":
        d+=1
      if key=='private' and item[key]:
        d+=1

      if (key=='latestPosts' and item[key]) or (key=='latestIgtvVideos' and item[key]) and item['followersCount']>1000 and item['private']=="False":
        c+=1
        for x in range(len(item[key])):
          if item[key][x]['likesCount']>10000 and str(item['username'])+"#with_chester_cheetah" in item[key][x]['hashtags'] and item['hasChannel']=="True":
            common+=1
    if common>0:
        Participated_Influencers+=1
    elif c>0:
        Eligible_influencers+=1

  return(Eligible_influencers,Participated_Influencers)
main()


