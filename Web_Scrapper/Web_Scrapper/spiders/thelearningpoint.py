# -*- coding: utf-8 -*-
import sys
import scrapy
from scrapy.exceptions import CloseSpider

class ThelearningpointSpider(scrapy.Spider):
	name = 'thelearningpoint'	
	allowed_domains = ["thelearningpoint.net"]	
	start_urls = []
	start_urls.extend(["http://www.thelearningpoint.net/system/app/pages/search?scope=search-site&q=school&offset=%d/" % i for i in range(10)])
	exit_flag = False

	download_dir = "output.csv" #where you want the file to be downloaded to 

	csv = open(download_dir, "w")  #"w" indicates that you're writing strings to the file

	columnTitleRow = "name, email\n"
	
	csv.write(columnTitleRow)

	def parse(self, response):	
		url_list = response.xpath('//h3/a/@href').extract();
		for url in url_list:
			absolute_url = response.urljoin(url)
			yield scrapy.Request(absolute_url,callback=self.parse_individual_school_details)
		
	def parse_individual_school_details(self, response):
		details = response.xpath('//div/b/font/text()').extract()
		start = 'Email:'
		end = ', '
		email_info_string = details[6]
		email= email_info_string[email_info_string.find(start)+len(start):email_info_string.rfind(end)]			
		print 'details:' + details +'\tname:' + details[0] + '\temail:' + eamil + '\t url:' + response.url
		yield {'name': details[0], 'url':response.url}
		#print 'ERROR'
		#sys.exit()	