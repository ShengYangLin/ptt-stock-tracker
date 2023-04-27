from typing import ByteString
import time
import requests
from pyquery import PyQuery as pq
from datetime import datetime
from backend.db import save_post_to_db
import yaml
from yaml.loader import SafeLoader


class Crawler:
    def __init__(self) -> None:

        with open('./config.yaml', encoding="utf-8") as f:
            config = yaml.load(f, Loader=SafeLoader)
            
        self.ptt_stock_url = config.get("pttStockUrl")
        self.celebrity_list = config.get("celebrityList", [])
        self.check_page_num = config.get("checkPageNum", 6)
        self.request_interval = config.get("requestInterval", 5)       
        self.key_transfer_dict = config.get("keyTransform", {})

    def process_post(self, post_object:dict) -> dict:
        result_obj = {"valid": True}
        post_url = post_object.get("url", "")
        if post_url:
            resp = requests.get(post_url)
            time.sleep(self.request_interval)
            if resp.status_code == 200:
                result_obj["url"] = post_url
                html_data = pq(resp.text)
                for item in html_data("#main-container #main-content .article-metaline").items():
                    tag = next(item(".article-meta-tag").items()).text()
                    value = next(item(".article-meta-value").items()).text()
                    key = self.key_transfer_dict[tag]
                    result_obj[key] = value
                
                push_result_list = []
                for item in html_data("#main-container #main-content .push").items():
                    try:
                        user_id = next(item(".push-userid").items()).text()
                        content = next(item(".push-content").items()).text()
                        push_time = next(item(".push-ipdatetime").items()).text()
                        if user_id in self.celebrity_list:
                            push_result_list.append(f"{user_id} {content} {push_time}")
                    except StopIteration as e:
                        continue
                if push_result_list or result_obj.get("author", "") in self.celebrity_list:
                    result_obj["push"] = push_result_list
                else:
                    result_obj["valid"] = False
        return result_obj

    def get_previous_page_and_posts(self, page_url) -> list:
        post_object_list = []
        previous_page_url = None
        resp = requests.get(page_url)
        if resp.status_code == 200:
            html_data = pq(resp.text)

            selector = "#main-container .action-bar .btn-group-paging"
            item = next(html_data(selector).items())
            previous_page_url = "https://www.ptt.cc/" + item('a:contains("上頁")').attr("href")

            selector = "#main-container .bbs-screen .r-ent"
            for item in html_data(selector).items():
                try:
                    popularity = next(item(".nrec").items()).text()
                    title = next(item(".title").items()).text()
                    post_url = "https://www.ptt.cc/" + next(item(".title a").items()).attr("href")
                    author = next(item(".author").items()).text()
                    # print(popularity, title, author, post_url)
                    post_object = {
                        "url": post_url,
                        "title": title,
                        "author": author,
                        "popularity": popularity
                    }
                    post_object_list.append(post_object)
                except Exception as e:
                    pass
        return previous_page_url, post_object_list
    
    def process_current_page(self, current_url:str) -> str:
        previous_page_url, post_object_list = self.get_previous_page_and_posts(current_url)
        for post_obj in post_object_list:
            result_post_obj = self.process_post(post_obj)
            save_post_to_db(result_post_obj)
        return previous_page_url

    def crawl(self):
        current_page_url = self.ptt_stock_url
        for i in range(0, self.check_page_num):
            current_page_url = self.process_current_page(current_page_url)
        
            

if __name__ == "__main__":
    crawler = Crawler()
    crawler.crawl()
