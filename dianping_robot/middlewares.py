import random
import logging

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from dianping_robot.settings import PROXIES
from dianping_robot.settings import USER_AGENTS
from scrapy.exceptions import IgnoreRequest


class RotateUserAgentMiddleware(UserAgentMiddleware):

    def process_request(self, request, spider):
        user_agent = random.choice(USER_AGENTS)
        if user_agent:
            request.headers.setdefault('User-Agent', user_agent)
            logging.debug('%s has been used' % user_agent)


class ProxyMiddleware(UserAgentMiddleware):

    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)
        request.meta['proxy'] = "http://%s" % proxy['ip_port']
        logging.debug('%s has been used' % proxy['ip_port'])
    # the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
    # for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php


class DuplicateFilterMiddleware(object):

    def __init__(self):
        self.url_has_seen = set()

    def process_request(self, request, spider):
        if request.url in self.url_has_seen:
            raise IgnoreRequest("Duplicate url found: %s" % request.url)
        else:
            self.url_has_seen.add(request.url)
