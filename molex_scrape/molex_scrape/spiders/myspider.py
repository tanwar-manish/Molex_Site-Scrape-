import scrapy

class MyspiderSpider(scrapy.Spider):
    name = "myspider"
    start_urls = [
        'https://www.molex.com/en-us/products/connectors/solderless-terminals?materialMaster_promotable=true&category_uid=solderless-terminals&page=1'
    ]

    custom_settings = {
        'FEEDS': {
            'molex_output.csv': {
                'format': 'csv',
                'fields': ['Website', 'Product URL', 'Product Count', 'Category Name', 'Category URL', 'Page Number'],
            },
        }
    }

    def parse(self, response):
        try:
            product_links = response.xpath('//*[@id="productlist-697e85dbef"]/div[2]/div[2]//h3/a/@href').extract()
            product_count = response.xpath('//*[@id="productlist-697e85dbef"]/div[1]/h4/text()').extract_first()

            category_name = 'Solderless Terminals'
            category_url = 'https://www.molex.com/en-us/products/connectors/solderless-terminals?materialMaster_promotable=true'

            #Page number
            current_page = int(response.url.split('=')[-1])

            for link in product_links:
                yield {
                    'Website': 'https://www.molex.com/',
                    'Product URL': response.urljoin(link),
                    'Product Count': product_count.strip() if product_count else '',
                    'Category Name': category_name,
                    'Category URL': category_url,
                    'Page Number': current_page
                }

            # Check if there are more pages to crawl
            if product_links:
                next_page = current_page + 1
                
                # Skip pages 132 and 158 (Both pages are blanked )
                if next_page not in [132, 158]:
                    next_page_url = f"https://www.molex.com/en-us/products/connectors/solderless-terminals?materialMaster_promotable=true&category_uid=solderless-terminals&page={next_page}"
                    yield scrapy.Request(next_page_url, callback=self.parse)
                else:
                    self.logger.info(f"Skipping processing for page {next_page}")
                    next_page += 1
                    next_page_url = f"https://www.molex.com/en-us/products/connectors/solderless-terminals?materialMaster_promotable=true&category_uid=solderless-terminals&page={next_page}"
                    yield scrapy.Request(next_page_url, callback=self.parse)

        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
