import scrapy
from jobs.items import JobItem
import autopager
import requests
import jobs.spiders.helpers

class JobsComSpider(scrapy.Spider):
    name = 'JobSpider'
    allowed_domains = []

    items_selector = ""
    url_pattern = ''

    pages = 1
    page_step = 1
    current_page = 1
    concurrent_requests = 5

    def start_requests(self):
        self.items_selector = self.job_detail
        self.url_pattern, self.pages, self.page_step = self.find_page_data(self.job_url)

        if self.page_step != 1:
            self.pages = self.pages / self.page_step + 1
        if self.concurrent_requests > self.pages:
            self.concurrent_requests = self.pages

        for i in range(self.concurrent_requests):
            url = self.url_pattern.format(self.page_num())
            self.current_page += 1
            yield scrapy.Request(url)

    def parse(self, response):
        for item_url in set(response.css(self.items_selector).getall()):
            item_url = response.urljoin(item_url)
            yield scrapy.Request(url=item_url, callback=self.parse_item)

        self.current_page += 1
        if self.current_page <= self.pages:
            next_page = self.url_pattern.format(self.current_page)
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_item(self, response):
        data = {
            "url": response.url,
            "raw_html": response.text
        }
        item_data = JobItem(data)
        yield item_data

    def page_num(self):
        if self.page_step == 1:
            return self.current_page
        else:
            return (self.current_page - 1) * self.page_step

    def find_page_data(self, url):
        res_arr = autopager.urls(requests.get(url))
        arr = []
        unique_str = set(res_arr)

        for number in unique_str:
            arr.append(number)

        while url in arr:
            arr.remove(url)
            
        n = len(arr)
        s = arr[1]
        l = len(s)
        pattern = ""

        for i in range(l):
            for j in range(i + 1, l + 1):
                stem = s[0:j]
                k = 1
                for k in range(1, n):
                    if stem not in arr[k]:
                        break
                if (k + 1 == n and len(pattern) < len(stem)):
                    pattern = stem

        sub_str = 0
        sub_arr = []
        sub_step = 0
        sub_ind = 0
        last_str = []

        for item in arr:
            sub_ind = len(pattern)
            while(sub_ind < len(item) and item[sub_ind] >= '0' and item[sub_ind] <= '9'):
                sub_ind+=1
            sub_str = max(int(sub_str), int(item[len(pattern): sub_ind]))
            sub_arr.append(int(item[len(pattern): sub_ind]))
            last_str.append(item[sub_ind:])

        sub_arr.sort()
        sub_step = sub_arr[0]

        if len(sub_arr) >= 3:
            sub_step = sub_arr[1] - sub_arr[0]

        return pattern + "{}", sub_str, sub_step, last_str[0]
