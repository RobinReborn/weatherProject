import scrapy
#from scrapy import Spider
from scrapy.selector import Selector
from Weather.items import WeatherItem

class WeatherSpider(scrapy.Spider):
	name = 'weather_spider'
	allowed_urls = ['https://www.wunderground.com/']
	#start_urls = ['https://www.wunderground.com/history/?MR=1']
	#this changes between scrapes
	start_urls = ['https://www.wunderground.com/history/airport/KLAX/1986/1/1/DailyHistory.html?']
	def verify(self, content):
		if isinstance(content, list):
			print "test verify\n"
			if len(content) > 0:
				content = content[0]
				 # convert unicode to str
				return content.encode('ascii','ignore')
			else:
				return ""
		else:
			# convert unicode to str
			return content.encode('ascii','ignore')

	#we have a class variable to count the iterations through the parse loop
	i=0
	def parse(self, response):
		# >>>>>>>> It is not a good practice to manually code the number. Is there any generic way to do it? <<<<<<<<
		if self.i < 10957:
			#we extract the date for the weather observations
			Date = response.xpath("//h2[@class='history-date']/text()").extract_first()
			#this gives us all the rows of our table
			rows = response.xpath('//div[@id="observations_details"]/table/tbody/tr')
			#this gives us the path to a link for the next day
			next_day = response.xpath('//div[@class="next-link"]/a/@href').extract_first()
			next_day_url = "https://www.wunderground.com"  + next_day

			# >>>>>>> Nice comments. <<<<<<<<
			for row in rows:
				#this gives us all the elements of the row, many of them are empty
				raw_data = row.xpath('.//text()').extract()
				#the rows are of variable length because sometimes windchill and gustspeed are present
				#sometimes windspeed takes two values (speed and 'mph') and sometimes it is just 'calm'
				#so we get rid of all the unnecessary info
				junkStrings = ['\n\t\t','\n  ',u'\xa0mph','\n',u'\n\t\xa0\n',u'\xa0\xb0F',u'\xa0mi']
				parsed_Data = filter(lambda a: a not in junkStrings, raw_data)
				time = parsed_Data[0]
				temperature = parsed_Data[1]
				offset = 0
				#the pattern I've found generally holds but there is some bad data on the website
				try:
					if (len(response.xpath('//div[@id="observations_details"]/table//th')) == 13):
						windChill = parsed_Data[2]
					else:
						windChill = "'"
						offset = -1
					# >>>>>>> To shorten the code, you might do dewPoint = self.verify(parsed_Data[3 + offset]0 <<<<<<<<<
					dewPoint = parsed_Data[3 + offset]
					humidity = parsed_Data[4+ offset]
					pressure = parsed_Data[5+ offset]
					visibility = parsed_Data[7+ offset]
					windDir = parsed_Data[8+ offset]
					windSpeed = parsed_Data[9+ offset]
					gustSpeed =parsed_Data[10+ offset]
					precipitation = parsed_Data[11+ offset]
					item = WeatherItem()
					time = self.verify(time)
					Date = self.verify(Date)
					temperature = self.verify(temperature)
					windChill = self.verify(windChill)
					dewPoint = self.verify(dewPoint)
					humidity = self.verify(humidity)
					pressure = self.verify(pressure)
					visibility = self.verify(visibility)
					windDir = self.verify(windDir)
					windSpeed = self.verify(windSpeed)
					gustSpeed = self.verify(gustSpeed)
					precipitation = self.verify(precipitation)
					item['time'] = time
					item['windChill'] = windChill
					item['temperature'] = temperature
					item['dewPoint'] = 	dewPoint
					item['humidity'] = humidity
					item['pressure'] = pressure
					item['visibility'] = visibility
					item['windDir'] = windDir
					item['windSpeed'] =  windSpeed
					item['gustSpeed'] = gustSpeed
					item['precipitation'] = precipitation
					item['Date'] = Date
					yield item
				except:
					continue
			self.i += 1
			yield scrapy.Request(next_day_url,callback=self.parse)
