#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser
import logging
import logging.config
import feedparser
import datetime
import mailer
from jinja2 import Environment, FileSystemLoader
from fuzzywuzzy import fuzz


def str2list(string):
    l = [ i for i in string.split('\n') if i ]
    return l

def is_updated_feed(feed, stale_date):
    '''
    whether the feed is updated or not
    '''
    try:
        feed_date = feed.feed.published_parsed
        #print  feed_date >= stale_date
        if feed_date >= stale_date:
            return True
        else:
            return False
    except:
        return True

def get_feed(feed_url):
    '''
    get list of feed objects from feed list
    '''
    feed_list = []
    for url in feed_url:
        feed = feedparser.parse(url)
        if is_updated_feed(feed, STALE_DATE):
            feed_list.append(feed)
        else:
            logger.warning('staled feed %s' % url)
    logger.info('get %s feeds from config file' % len(feed_list))
    return feed_list

def is_updated_entry(entry, stale_date):
    '''
    whether the entry is updated or not
    '''
    try:
        entry_date = entry.published_parsed
        #print entry_date >= stale_date
        if entry_date >= stale_date:
            return True
        else:
            return False
    except:
        return False

def get_entry(feed):
    '''
    get list of entries from feed
    '''
    entry_list = []
    for e in feed.entries:
        if is_updated_entry(e, STALE_DATE):
            entry_list.append((e.get('link'), e.get('title')))
            logger.info('valid entry %s' % e.get('title'))
        else:
            pass
            #logger.warning('staled entry %s' % e.get('title'))
    try:
        logger.info('get %s entries from %s' % (len(entry_list), feed.feed.title))
    except:
        logger.info('get %s entries' % len(entry_list))
    return entry_list

def get_entries(flist):
    '''
    get lists of entries from all feeds
    '''
    entries= {}
    for i in get_feed(flist):
        entry = get_entry(i)
        try:
            if entry:
                for e in entries:
                    for k in entry:
                        for j in entries[e]:
                            if fuzz.ratio(j[1], k[1]) > 95:
                                entry.remove(k)
                                logger.info('remove duplicate %s from %s' % (k[1], i.feed.title))
                entries[i.feed.title] = entry
        except:
            continue
    logger.info('get %s entries from %s feeds' % (len(entries), len(flist)))
    return entries

def get_content(template_dir, template_file, flist):
    env = Environment(loader=FileSystemLoader(template_dir))
    t = env.get_template(template_file)
    s = t.render(d=get_entries(flist))
    logger.info('generate html source successfully')
    return s


CONFIG_FILE = './xrss.conf'

config = ConfigParser.RawConfigParser()
config.read(CONFIG_FILE)
logging.config.fileConfig(CONFIG_FILE)
logger = logging.getLogger('xrss')

FEED_LIST = str2list(config.get('xrss', 'urls'))
TEMPLATE_DIR = config.get('xrss', 'template_dir')
TEMPLATE_FILE = config.get('xrss', 'template_file')
STALE_DATE = (datetime.datetime.now() -
    datetime.timedelta(days=config.getint('xrss', 'stale_date'))).timetuple()

#print str2list(config.get('xrss', 'recipients'))
html=get_content(TEMPLATE_DIR, TEMPLATE_FILE, FEED_LIST)
f = open('/tmp/o.html', 'w+')
f.write(html.encode('utf8'))
f.close()

try:
    mailer.send(
        subject='News from xRSS', 
        addresser=config.get('mail', 'addresser'),
        passwd=config.get('mail', 'passwd'),
        recipients= str2list(config.get('xrss', 'recipients')),
        html=get_content(TEMPLATE_DIR, TEMPLATE_FILE, FEED_LIST))
    logger.info('send news successfully')
except:
    logger.error('send news failed')
