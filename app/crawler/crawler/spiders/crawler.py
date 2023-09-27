import scrapy
import json

class QuotesSpider(scrapy.Spider):
    name = "crawler"
    all_article_data = []

    def start_requests(self):
        urls = [
            "https://magiskzip.com/category/gsi-rom/",
            "https://magiskzip.com/category/magisk-modules/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Extract all <article> elements with different IDs
        article_elements = response.css('article[id^="post-"]')

        for article in article_elements:
            # Extract the article's ID
            article_id = article.attrib['id']

            # Extract the text content of <h2> and <p> elements
            h2_text = article.xpath('.//h2/a/text()').get()
            p_text = article.xpath('.//p/text()').get()
            url_text = article.xpath('.//h2/a/@href').get()
            image = article.css('article a img::attr(src)').get()

            # Remove newline character from the title
            h2_text = h2_text.replace('\n', '')

            # Create a dictionary to store the extracted data
            data_dict = {
                "url": url_text,
                "article_id": article_id,
                "article_title": h2_text,
                "article_images": image,
                "article_content": p_text,
            }


            # Append the data to the list
            self.all_article_data.append(data_dict)

    def closed(self, reason):

        # Save all article data as a single JSON file
        filename = f"saved_templates/all_articles.json"

        # saves the json file to store the extracted data   
        with open(filename, "w", encoding="utf-8") as json_file:
            json.dump(self.all_article_data, json_file, indent=4, ensure_ascii=False)

        self.log(f"Saved JSON file {filename}")

    """ def get_sanitized_title(self, response):
        # Extract the title from the HTML response
        title = response.css('title::text').get().strip()

        # Remove any invalid characters from the title to use it in the filename
        sanitized_title = "".join(c for c in title if c.isalnum() or c.isspace()).rstrip()

        return sanitized_title """
