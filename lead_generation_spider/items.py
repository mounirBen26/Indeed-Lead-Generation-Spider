# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LeadGenerationSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    linkedin_url = scrapy.Field()
    title = scrapy.Field()
    headline = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    email_status = scrapy.Field()
    email = scrapy.Field()
    twitter_url = scrapy.Field()
    facebook_url = scrapy.Field()
    company_name = scrapy.Field()
    company_address = scrapy.Field()
    phone = scrapy.Field()
    website = scrapy.Field()
