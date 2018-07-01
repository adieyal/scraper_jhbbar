import scrapy
from dateutil import parser
from datetime import datetime
from jhb_bar.items import Member
from jhb_bar.scrapy_logger import get_logger

def eorz(x):
    return x[0].strip() if x else None

def dateorz(x):
    try:
        if type(x) == list:
            x = x[0]
        return parser.parse(x)
    except (ValueError, TypeError, IndexError):
        return None

class MembersSpider(scrapy.Spider):
    name = "members"
    item = Member

    def __init__(self, *args, **kwargs):
        self.logger.logger = get_logger(MembersSpider.name)
        return super(MembersSpider, self).__init__(*args, **kwargs)
    
    def start_requests(self):
        self.logger.info("Started Johannesburg Bar spider")
        urls = [
            'https://johannesburgbar.co.za/contact-details-of-all-members/',
            'https://johannesburgbar.co.za/contact-details-of-junior-members/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_lawyers(self, response):
        member = Member()

        for chunk in response.css(".pf-content").xpath(".//p"):
            member = Member(
                name=chunk.xpath("normalize-space(./strong[1]/text())").extract_first(),
                group=chunk.xpath("normalize-space(./strong[2]/text())").extract_first(),
                email=chunk.xpath("./a/text()").extract_first(),
                phone=eorz(chunk.xpath(".//text()[3]").re(r"Phone Number: ([^\xa0]*).*Fax")),
                fax=eorz(chunk.xpath(".//text()[3]").re(r"Fax Number: ([^\xa0]*).*Cell")),
                cell=eorz(chunk.xpath(".//text()[3]").re(r"Cell Number: ([^\xa0]*)")),
                member_type="junior" if "junior" in response.url else "silk",
                scraped_date=datetime.now()
            )
            
            tip_anchor = chunk.xpath("./a/@id").extract_first()
            if tip_anchor:
                tip = chunk.xpath("//div[contains(@data-anchor, '" + tip_anchor + "')][1]")
                member["admitted"] = dateorz(tip.re("Admitted: ([^ ]*)<br>"))
                member["society"] = dateorz(tip.re("Society: ([^ ]*)<br>"))
                member["silk"] = dateorz(tip.re(r"Silk: ([^ ]*)(?:\n|<br>)"))
                member["seniority"] = dateorz(tip.re(r"Seniority: ([^ ]*)(?:\n|<br>)"))

            yield member

        for href in response.xpath("//ul[contains(@class, 'frm_pagination')]//a/@href").extract():
            yield response.follow(href, self.parse_lawyers)

    def parse(self, response):
        for href in response.xpath('//*[@id="main"]/div[2]/div/main/article/div/div/div/div[1]/div/a/@href').extract():
            yield response.follow(href, self.parse_lawyers)
