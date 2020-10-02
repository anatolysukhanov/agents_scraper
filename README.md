# QuotesBot
This is a Scrapy (see https://docs.scrapy.org/en/latest/index.html) project to scrape agents from https://agents.allstate.com/usa/fl.

## Extracted data

This project extracts agents and utilizes Google Maps Geocoding API to geocode the addresses.

The output data looks like this sample:

    {
        "name": "Hugh L. Cain", 
        "phone": "(352) 371-5777", 
        "address1": "16181 NW US Hwy 441", 
        "address2": "Unit 180", 
        "city": "Alachua", 
        "postal": "32615", 
        "lat": 29.8055057,
        "lng": -82.5216834
    }

## Spider

This project contains one spider and you can see it using the `list` command:

    $ scrapy list
    css-scraper

The spiders extracts the data employing CSS selectors.

## Running the spider

You can run the spider using the `scrapy crawl` command, such as:

    $ scrapy crawl css-scraper

If you want to save the scraped data to a file, you can pass the `-o` option:
    
    $ scrapy crawl css-scraper -o quotes.json
