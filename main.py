# -*- coding: utf-8 -*-
import facebook
import feedparser
import time
import conf
import mail_remind
import datetime
import log_func


rss_link="https://autoconsulting.com.ua/rss.html"
list_of_articles = []
Filename_of_article_list = "List_of_articles_in_fb.txt"
logfile = log_func.logfile

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

def search_for_quots(title_text):
    while (title_text.find('&quot;')!=-1):
        title_text_copy=title_text
        title_text=title_text_copy[:title_text.find('&quot;')]+'"'+title_text[title_text.find('&quot;')+6:]
    return title_text

def input_already_list_in_script(filename):
    with open(filename, 'r') as f:
        list_from_file = f.read().splitlines()
        if (len(list_from_file)>50): list_from_file = list_from_file[len(list_from_file)-40:]
    return list_from_file


if __name__ == '__main__':
    try:
                fb = facebook.GraphAPI(access_token=conf.page_token)
                #parse_autocon(list_of_articles,rss_link,Filename_of_article_list)

                list_of_articles = input_already_list_in_script(Filename_of_article_list)
                feed = feedparser.parse(rss_link)
                mail_remind.compare_last_mod_date()
                for entry in feed.entries:
                    article_title = entry.title
                    if list_of_articles.count(article_title) == 0:
                            article_link = entry.link
                            print(article_link)
                            print(article_title)
                            try:
                                attachments = {'link': article_link }
                                fb.put_wall_post(profile_id="209397329409982", message="Подписывайтесь на нашу рассылку новостей в Telegram\nt.me/autoconsulting", attachment=attachments)
                                #fb.put_wall_post(profile_id="332886790816613", message="Подписывайтесь на нашу рассылку новостей в Telegram\nt.me/autoconsulting", attachment=attachments)
                                with open(Filename_of_article_list, 'a') as f:
                                    f.write(article_title+ '\n')
                                    list_of_articles.append(article_title)
                            except Exception as ex:
                                log_func.logging(logfile,ex)

    except Exception as ex:
        log_func.logging(logfile,ex)