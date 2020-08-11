## @package main
#  This module responsible for parsing website and publish it on Facebook page

# -*- coding: utf-8 -*-
import facebook
import feedparser
import time
import conf
import mail_remind
import log_func

rss_link="http://agropravda.com/feed"
list_of_articles = []
Filename_of_article_list = "List_of_articles_in_fb.txt"
logfile = log_func.logfile

## Parse website by 'rss_link' and put aviable article titles into file 'filename'
#   param list a List
#   param rss_link a string
#   param filename a string
#   No return
def parse_autocon(list,rss_link,filename):
    try:
        with open(filename,'a') as f:
            feed = feedparser.parse(rss_link)
            for entry in feed.entries:
                time.sleep(5)
                article_title = search_for_quots(entry.title)
                f.write(article_title+'\n')

    except Exception:
        print(time.strftime("%H:%M", time.localtime()) + "  Error parse")

## Get text and transform symbol set '&quot' into '"'
#   param title_text a string
#   return string
def search_for_quots(title_text):
    while (title_text.find('&quot;')!=-1):
        title_text_copy=title_text
        title_text=title_text_copy[:title_text.find('&quot;')]+'"'+title_text[title_text.find('&quot;')+6:]
    return title_text

## Convert file 'filename' into List and cut it if list too long
#   param filename a string
#   return List
def input_already_list_in_script(filename):
    with open(filename, 'r') as f:
        list_from_file = f.read().splitlines()
        if (len(list_from_file)>50): list_from_file = list_from_file[len(list_from_file)-40:]
    return list_from_file

if __name__ == '__main__':
    ###Uncomment this part is to check if program have permissions to write into logfile and Listfile
    #log_func.logging(logfile,"Program has permissions to write into logfile")
    #with open(Filename_of_article_list, 'a') as f:
        #f.write('Program has permissions to write into listfile\n')

    try:
                fb = facebook.GraphAPI(access_token=conf.page_token)
                #parse_autocon(list_of_articles,rss_link,Filename_of_article_list)

                list_of_articles = input_already_list_in_script(Filename_of_article_list)
                feed = feedparser.parse(rss_link)
                #mail_remind.compare_last_mod_date()
                for entry in feed.entries:
                    article_title = entry.title
                    if list_of_articles.count(article_title) == 0:
                            article_link = entry.link
                            try:
                                attachments = {'link': article_link }
                                fb.put_wall_post(profile_id="605349992829039", message="Подписывайтесь на нашу рассылку новостей в Telegram\nt.me/agropravda", attachment=attachments)
                                with open(Filename_of_article_list, 'a') as f:
                                    f.write(article_title+ '\n')
                                    list_of_articles.append(article_title)
                            except Exception as ex:
                                print(ex)
                                log_func.logging(logfile,ex)

    except Exception as ex:
        print(ex)
        log_func.logging(logfile,ex)