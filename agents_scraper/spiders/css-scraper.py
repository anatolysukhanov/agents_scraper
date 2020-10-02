import scrapy
import googlemaps


class Geocoder():
    key = 'AIzaSyBAWruKe5GxiXemypOczyG_0XejNMv6wBY'
    gmaps = googlemaps.Client(key=key)

    def geocode(self, address):
        geocode_result = self.gmaps.geocode(address)
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        return [lat, lng]


class CSSScraperSpider(scrapy.Spider):
    name = "css-scraper"
    start_urls = [
        'https://agents.allstate.com/usa/fl'
    ]
    geocoder = Geocoder()

    def parse_teaser(self, response):
        for article in response.css("article"):
            address1 = article.css("span.c-address-street-1::text").extract_first()
            address2 = article.css("span.c-address-street-2::text").extract_first()
            city = article.css("span.c-address-city::text").extract_first()
            postal = article.css("span.c-address-postal-code::text").extract_first()
            address = address1 + (" " + address2 if address2 else "") + city + " " + postal
            (lat, lng) = self.geocoder.geocode(address)
            yield {
                'name': article.css("span.Teaser-name::text").extract_first(),
                'phone': article.css("span.Teaser-phoneText::text").extract_first(),
                'address1': address1,
                'address2': address2,
                'city': city,
                'postal': postal,
                'lat': lat,
                'lng': lng
            }

    def parse_hero(self, response):
        address1 = response.css("span.c-address-street-1::text").extract_first()
        address2 = response.css("span.c-address-street-2::text").extract_first()
        city = response.css("span.c-address-city::text").extract_first()
        postal = response.css("span.c-address-postal-code::text").extract_first()
        address = address1 + (" " + address2 if address2 else "") + city + " " + postal
        (lat, lng) = self.geocoder.geocode(address)
        yield {
            'name': response.css("span.Hero-name::text").extract_first(),
            'phone': response.css("span.Core-phoneText::text").extract_first(),
            'address1': address1,
            'address2': address2,
            'city': city,
            'postal': postal,
            'lat': lat,
            'lng': lng
        }

    def parse(self, response):
        for link in response.css("a.Directory-listLink::attr(href)"):
            url = link.extract().replace("../", "https://agents.allstate.com/")
            if (url.endswith(".html")):
                yield scrapy.Request(url, callback=self.parse_hero)
            else:
                yield scrapy.Request(url, callback=self.parse_teaser)
