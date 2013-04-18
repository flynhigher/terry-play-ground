__author__ = 'tgo'
from scrapy.spider import BaseSpider
from scrapy.http import FormRequest, Request
from scrapy.selector import HtmlXPathSelector

class NjmlsSpider(BaseSpider):
    name = "njmls"
    #allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.newjerseymls.com"
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        form = hxs.select('//form[@id="frmEntry"]')
        if form:
            return [FormRequest(url='http://www.priv.njmls.xmlsweb.com/login_new.asp',
                                formdata={'board': 'T',
                                          'usid': 'seung+y.+nam',
                                          'pass_temp': 'Password',
                                          'password': ''},
                                callback=self.validate)]
        else:
            self.log('Failed to get homepage')
            filename = response.url.split("/")[-1]
            if not filename:
                filename = 'home'
            open(filename, 'wb').write(response.body)

    def validate(self, response):
        hxs = HtmlXPathSelector(response)
        form = hxs.select('//form[@id="frmEntry"]')
        if form:
            return [FormRequest(url='http://www.priv.njmls.xmlsweb.com/validate.asp',
                                formdata={'usid=seung+y.+nam',
                                          'password=n9436016',
                                          'vista=Y',
                                          'height=1600'},
                                callback=self.get_report_form)]
        else:
            self.log('Failed to login')
            filename = response.url.split("/")[-1]
            open(filename, 'wb').write(response.body)

    def get_report_form(self, response):
        hxs = HtmlXPathSelector(response)
        title = hxs.select('//title/text()')
        if title == 'Object moved':
            return [Request('http://www.priv.njmls.xmlsweb.com/StatisticsReports/default.asp?frommenu=1',
                            self.submit_report_form)]
        else:
            self.log('Failed to validate')
            filename = response.url.split("/")[-1]
            open(filename, 'wb').write(response.body)

    def submit_report_form(self, response):
        hxs = HtmlXPathSelector(response)
        title = hxs.select('//title/text()')
        if title == 'Statistics Reports':
            return [FormRequest(url='http://www.priv.njmls.xmlsweb.com/StatisticsReports/Reports/StatisticsReport.asp',
                                formdata={'reportType': 'stats',
                                          'reportScope': 'MLS',
                                          'ShowSQL': 'N',
                                          'whichdate': 'S',
                                          'OfficeCode': '56702',
                                          'AgentCode': '1008233',
                                          'BeginDate': '1%2F1%2F2012',
                                          'EndDate': '1%2F31%2F2012',
                                          'PropType': '1',
                                          'Areacode': '2',
                                          'Cnty_Locale': '',
                                          'Subarea': '0201',
                                          'Statuscode': '',
                                          'Statuscode2': '',
                                          'sale_lease': '',
                                          'CurPrice': '',
                                          'CurPrice': '',
                                          'Bedrooms': '',
                                          'Bedrooms': '',
                                          'Fullbaths': '',
                                          'Fullbaths': '',
                                          'Half_bath': '',
                                          'Half_bath': '',
                                          'Style': '',
                                          'Bldg_Complex': '',
                                          'StreetNum': '',
                                          'StreetNum': '',
                                          'StreetNumTxt': '',
                                          'StreetName': '',
                                          'StreetDir': '',
                                          'StrMode': ''},
                                callback=self.extract_data)]
        else:
            self.log('Failed to get report form')
            filename = response.url.split("/")[-1]
            open(filename, 'wb').write(response.body)

    def extract_data(self, response):
        hxs = HtmlXPathSelector(response)
        name = hxs.select('//td[@align="left" && @class="statsTitle"]/text()')
        if name == 'Seung Y. Nam':
            self.log('Success')
        else:
            filename = response.url.split("/")[-1]
            open(filename, 'wb').write(response.body)
