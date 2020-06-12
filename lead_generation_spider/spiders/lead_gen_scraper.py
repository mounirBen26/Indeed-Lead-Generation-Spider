import scrapy
from scrapy import Request
import re,time, requests,json
from lead_generation_spider.items import LeadGenerationSpiderItem

class LeadgenrationSpider(scrapy.Spider):
    name="lead_gen_bot"
    
    def __init__(self,start_urls,api_key, *args, **kwargs):
        super(LeadgenrationSpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls.split(',')
        self.api_key = api_key


    def start_requests(self):
        start_urls = self.start_urls
        for url in start_urls:
            yield Request(url, callback=self.parse)
    
    def parse(self,response):
        job_titles = ['HR manager','Director of HR', 'vp of HR','CEO','Head of']
        company_titles = response.xpath('//a[@class="turnstileLink"]/text()').extract()
        for job in job_titles:
            for company in company_titles:
                yield Request('https://search.yahoo.com/search;?p='+requests.compat.quote_plus('"{} at {}" site:linkedin.com'.format(job,company)),
                              callback = self.scrape_api, meta={'company_name':company,'title':job})
    
    def scrape_api(self,response):
        profile_titles = response.xpath('//h3/a/text()').extract()
        for profile in profile_titles:
            value = profile.split('-')[0]
            if '|' or '...' not in value:
                profile_name = value 
                headers = {
                    'Content-Type': 'application/json',
                    'Cache-Control': 'no-cache',
                }
                try:
                    data = {"api_key": self.api_key, "first_name": "","last_name": "", "organization_name": ""}
                    data["first_name"], data["last_name"], data["organization_name"] = profile_name.split()[0], profile_name.split()[-1], response.meta['company_name'].strip()
                    api_resp = requests.post('https://api.apollo.io/v1/people/match', headers=headers, data=json.dumps(data))
                    email = api_resp.json().get('person').get('email')
                    if email:
                        item = LeadGenerationSpiderItem(
                            first_name = api_resp.json().get('person').get('first_name'),
                            last_name = api_resp.json().get('person').get('last_name'),
                            linkedin_url = api_resp.json().get('person').get('linkedin_url'),
                            title = api_resp.json().get('person').get('title'),
                            headline = api_resp.json().get('person').get('headline'),
                            city = api_resp.json().get('person').get('city'),
                            state = api_resp.json().get('person').get('state'),
                            email_status = api_resp.json().get('person').get('email_status'),
                            email = email,
                            twitter_url = api_resp.json().get('person').get('twitter_url'),
                            facebook_url = api_resp.json().get('person').get('facebook_url'),
                            company_name = api_resp.json().get('person').get('organization').get('name'),
                            company_address = api_resp.json().get('person').get('organization').get('raw_address'),
                            phone = api_resp.json().get('person').get('organization').get('phone'),
                            website = api_resp.json().get('person').get('organization').get('website_url')
                        )
                        yield item
                except Exception as e:
                    print('Error!, Maybe API has ran out of credits!',e)
                    
                    
                              
        
        