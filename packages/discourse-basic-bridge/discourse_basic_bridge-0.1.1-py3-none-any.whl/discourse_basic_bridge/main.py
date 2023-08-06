import json
import requests
from requests.structures import CaseInsensitiveDict
import urllib.parse
from urllib.parse import urlparse
import random

global ENV_URL
global ENV_BOT_NAME
global ENV_COOKIE
global ENV_CSRF

def get_domain(url, with_protocall=True):
  ''' defining function to get the domain '''
  try:
    url = urlparse(url)
    return f"{url.scheme}://{url.netloc}" if with_protocall else url.netloc # --> www.example.test or https://www.example.test
  except Exception as error:
    return error

url = ENV_URL
get_basic_url = url+'.json'
get_all_posts_url = url+'.json?print=true'
post_url = get_domain(url)+'/posts'


headers = CaseInsensitiveDict()

#Fixed headers
headers["discourse-present"] = "true"
headers["sec-ch-ua-mobile"] = "?1"
headers["discourse-logged-in"] = "true"
headers["content-type"] = "application/x-www-form-urlencoded; charset=UTF-8"
headers["accept"] = "*/*"
headers["x-requested-with"] = "XMLHttpRequest"
headers["sec-fetch-site"] = "same-origin"
headers["sec-fetch-mode"] = "cors"
headers["sec-fetch-dest"] = "empty"
headers["accept-language"] = "en-US,en;q=0.9"
headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Headers to change
headers["authority"] = get_domain(url, with_protocall=False)
headers["x-csrf-token"] =  ENV_CSRF
headers["origin"] = get_domain(url)
headers["referer"] = get_domain(url) + '/'
headers["cookie"] = ENV_COOKIE
bot_name = ENV_BOT_NAME

def get_basic_info_of_thread():
  '''defining a function to get the basic info of the thread'''
  try:
    r = requests.get(get_basic_url, headers=headers)
    open('file.json', 'wb').write(r.content)
  except Exception as error:
    return error
  return r

content = json.loads(get_basic_info_of_thread().content)

category = content['category_id']
topic_id = content['id']
typing_duration_msecs = random.randint(1000,10000)
composer_open_duration_msecs = random.randint(1000,10000)

def get_content_thread():
  '''defining function to get the content from the thread'''
  try:
    r = requests.get(get_posts_url, headers=headers)
    open('file.json', 'wb').write(r.content)
  except Exception as error:
    return error
  return r
  
def detect_ping():
  '''defining a function to detect if someone pings the bot'''
  try:
    r = get_content_thread()
    p = []
    data = json.loads(r.content)
    for post in data['post_stream']['posts']:
      if post['cooked'].rfind('@'+bot_name) != -1:
        p.append(post)
    return p
  except Exception as error:
    return error

def detect_last_ping():
  '''defining a function to detect the last ping to the bot'''
  try:
    pings = detect_ping()
    return pings[-1]
  except Exception as error:
    return error

 
def post_message_to_thread(message):
  '''defining a function for posting messages to the thread'''
  try:
    message = urllib.parse.quote_plus(message)
    data = 'raw='+str(message)+'&unlist_topic=false&category='+str(category)+'&topic_id='+str(topic_id)+'&is_warning=false&archetype=regular&typing_duration_msecs='+str(typing_duration_msecs)+'&composer_open_duration_msecs='+str(composer_open_duration_msecs)+'&featured_link=&shared_draft=false&draft_key=topic_4368&nested_post=true'
    p = requests.post(post_url, headers=headers, data=data)
  except Exception as error:
    return error
  return p

  if __name__=='__main__':
    pass