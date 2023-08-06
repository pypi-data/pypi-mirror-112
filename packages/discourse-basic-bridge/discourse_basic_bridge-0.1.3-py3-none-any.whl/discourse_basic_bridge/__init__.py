__version__ = '0.1.3'

from urllib.request import urlopen
import requests
import json
import requests
from requests.structures import CaseInsensitiveDict
import urllib.parse
from urllib.parse import urlparse
import random

class Bridge:
    
    def get_domain(self, url, with_protocall=True):
        try:
            url = urlparse(url)
            return f"{url.scheme}://{url.netloc}" if with_protocall else url.netloc # --> www.example.test or https://www.example.test
        except Exception as error:
            return error

    def __init__(self, ENV_URL, ENV_BOT_NAME, ENV_COOKIE, ENV_CSRF):
        self.ENV_URL = ENV_URL
        self.ENV_BOT_NAME = ENV_BOT_NAME
        self.ENV_COOKIE = ENV_COOKIE
        self.ENV_CSRF = ENV_CSRF
        self.url = ENV_URL
        self.get_basic_url = self.url+'.json'
        self.get_all_posts_url = self.url+'.json?print=true'
        self.post_url = self.get_domain(self.url)+'/posts'

        self.headers = CaseInsensitiveDict()

        #Fixed headers
        self.headers["discourse-present"] = "true"
        self.headers["sec-ch-ua-mobile"] = "?1"
        self.headers["discourse-logged-in"] = "true"
        self.headers["content-type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        self.headers["accept"] = "*/*"
        self.headers["x-requested-with"] = "XMLHttpRequest"
        self.headers["sec-fetch-site"] = "same-origin"
        self.headers["sec-fetch-mode"] = "cors"
        self.headers["sec-fetch-dest"] = "empty"
        self.headers["accept-language"] = "en-US,en;q=0.9"
        self.headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

        # Headers to change
        self.headers["authority"] = self.get_domain(self.url, with_protocall=False)
        self.headers["x-csrf-token"] =  ENV_CSRF
        self.headers["origin"] = self.get_domain(self.url)
        self.headers["referer"] = self.get_domain(self.url) + '/'
        self.headers["cookie"] = ENV_COOKIE
        self.bot_name = ENV_BOT_NAME
        try:
            r = requests.get(self.get_basic_url, headers=self.headers)
            content = json.loads(r.content)
            category = content['category_id']
            topic_id = content['id']
            typing_duration_msecs = random.randint(1000,10000)
            composer_open_duration_msecs = random.randint(1000,10000)
        except Exception as error:
            print(error)

    def get_content_thread(self):
        try:
            r = requests.get(self.get_posts_url, headers=self.headers)
            open('file.json', 'wb').write(r.content)
        except Exception as error:
            return error
        return r
  
    def detect_ping(self):
        try:
            r = self.get_content_thread()
            p = []
            data = json.loads(r.content)
            for post in data['post_stream']['posts']:
                if post['cooked'].rfind('@'+self.bot_name) != -1:
                    p.append(post)
            return p
        except Exception as error:
            return error

    def detect_last_ping(self):
        try:
            pings = self.detect_ping()
            return pings[-1]
        except Exception as error:
            return error

 
    def post_message_to_thread(self, message):
        try:
            message = urllib.parse.quote_plus(message)
            data = 'raw='+str(message)+'&unlist_topic=false&category='+str(self.category)+'&topic_id='+str(self.topic_id)+'&is_warning=false&archetype=regular&typing_duration_msecs='+str(self.typing_duration_msecs)+'&composer_open_duration_msecs='+str(self.composer_open_duration_msecs)+'&featured_link=&shared_draft=false&draft_key=topic_4368&nested_post=true'
            p = requests.post(self.post_url, headers=self.headers, data=data)
        except Exception as error:
            return error
        return p
