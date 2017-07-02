'''
 * Scrapy code for scrapping thelearningpoint.net
 * An EduGorilla assignment task for internship selection
 * Author: P Jishnu Jaykumar

 NOTE : Both the bonus points are taken care of

 		Bonus point (1) 
 		Following code will scrap the first 10 pages as mentioned in the task criteria
        and if the code is not able to parse any one of the links, 
        then it will fail gracefully by printing 
        the error message : Couldn't parse one of the links, hence crawling terminated

        Bonus point (2) 
        Scrapy framework is used for this assignment.

'''

import re
import scrapy
from scrapy.exceptions import CloseSpider

class ThelearningpointSpider(scrapy.Spider):
	name = 'thelearningpoint'
	allowed_domains = ["thelearningpoint.net"]	
	start_urls = []
	start_urls.extend(["http://www.thelearningpoint.net/system/app/pages/search?scope=search-site&q=school&offset=%d/" % i for i in range(10)])
	
	def parse(self, response):	
		url_list = response.xpath('//h3/a/@href').extract();
		for url in url_list:
			absolute_url = response.urljoin(url)
			yield scrapy.Request(absolute_url,callback=self.parseDetails)
	
	'''		
	Following function will parse the name and email details of schools 
	If details in any one of the search result's link is not parsed then 
	the spider will stop execution with the
	message:'Couldn't parse one of the links, hence crawling terminated'.
	'''		

	def parseDetails(self, response):
		
		try:
			details = response.xpath('//div/b/font/text()').extract()
			email = self.extractSubString(details[6],'Email:', ', ');

			#yield only if it(email) is a valid email address
			if(self.isValidEmail(email)):
				yield {'name': details[0], 'email':email}

		except IndexError:
			raise CloseSpider("Couldn't parse one of the links, hence crawling terminated.")
	
	'''
	Following function extracts a particular substring from the input string(inputStr)
	between the starting string(start) and ending string(end)
	'''
	
	def extractSubString(self,inputStr,start,end):
		return inputStr[inputStr.find(start)+len(start):inputStr.rfind(end)]			


	'''
	Following function makes sure that the parsed email string is
	actually following the email address format
	'''

	def isValidEmail(self, email):
		if(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email, flags=0)):
			return True
		else:
			return False

				