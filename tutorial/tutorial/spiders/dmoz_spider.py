import urllib
import os
from scrapy.spider import Spider
from scrapy.selector import Selector
from UserString import MutableString
class DmozSpider(Spider):
    name = "dmoz"
    allowed_domains = ["slideshare.net"]
    start_urls = [
        "http://www.slideshare.net/VentureSquare/ss-23085640"
    ]

    def parse(self, response):
    	self.foldername = response.url.split("/")[-2]
        filename = response.url.split("/")[-1]
        sel = Selector(response)
        sites = sel.css(".slide_container div img")
        for site in sites:
        	print(" ")
	        url = site.xpath('@data-full').extract()[0]
	        filename = os.path.basename(url)
	        filename = filename.split('?')[0]
	        print(url)
	        self.download_photo(url,filename)

    def download_photo(self, img_url, filename):
	    try:
			image_on_web = urllib.urlopen(img_url)
		        if image_on_web.headers.maintype == 'image':
					buf = image_on_web.read()
					path = MutableString()
					path = os.getcwd()+ "/files/" + self.foldername
					file_path = MutableString()
					file_path = path + "/" + filename
					self.makedir(path)
					downloaded_image = file(file_path, "wb")
					downloaded_image.write(buf)
					downloaded_image.close()
					image_on_web.close()
		        else:
		            return False    
	    except:
	        return False
	    return True

    def makedir(self,path):
    	if not os.path.exists(path): os.makedirs(path)