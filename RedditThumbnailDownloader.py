from bs4 import BeautifulSoup
import requests
import urllib2
import os

ORIGINAL_URL = "https://www.reddit.com/r/"


def download_all_pictures_to_path(output_path, subreddit_name, number_of_pages):
    url = ORIGINAL_URL + subreddit_name
    if output_path != '':
        if not os.path.exists(output_path):
            os.makedirs(output_path)
    try:
        for i in xrange(number_of_pages):
            print "\n------------------------------------------------------------------------"
            print "Source:", url
            print "------------------------------------------------------------------------\n"


            source_code = requests.get(url)

            #in case site fucking with me (blocking me)
            while source_code.status_code != 200:
                source_code = requests.get(url)
            content = source_code.content
            soup = BeautifulSoup(content, "html.parser")
            for pic_box in soup.findAll('a', {'class': 'thumbnail may-blank outbound'}):
                pic_url = pic_box.contents[0][u'src']
                file_name = pic_url.split("redditmedia.com/", 1)[1]

                if not os.path.exists(output_path + "/" + file_name):
                    print "Downloading", file_name, "\n"
                    resource = urllib2.urlopen("https:" + pic_url)
                    if output_path == '':
                        file_path = file_name
                    else:
                        file_path = output_path + "/" + file_name
                    try:
                        output_file = open(file_path, "wb")
                        output_file.write(resource.read())
                        output_file.close()
                    except:
                        try:
                            os.remove(file_path)
                        except OSError:
                            pass
                else:
                    print file_name, " Already taken\n"
            for pic_box in soup.findAll('a', {'class': 'thumbnail may-blank '}):
                pic_url = pic_box.contents[0][u'src']
                file_name = pic_url.split("redditmedia.com/", 1)[1]

                if not os.path.exists(output_path + "/" + file_name):
                    print "Downloading", file_name, "\n"
                    resource = urllib2.urlopen("https:" + pic_url)
                    if output_path == '':
                        file_path = file_name
                    else:
                        file_path = output_path + "/" + file_name
                    output_file = open(file_path, "wb")
                    output_file.write(resource.read())
                    output_file.close()
                else:
                    print file_name, " Already taken\n"
            try:
                url = soup.find('span', {'class' : 'next-button'}).find('a')['href']
            except Exception as ex:
                print ex, "\n"
        print "Done"
    except Exception as ex:
        print ex, "\n"
subreddit_name = raw_input("Enter subreddit name: ")
output_path = raw_input("Enter Output Path: ")
pages = input("Enter number of pages to parse from: ")
download_all_pictures_to_path(output_path, subreddit_name, pages)