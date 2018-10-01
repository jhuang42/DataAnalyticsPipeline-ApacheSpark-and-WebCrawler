from urllib.request import urlopen
from selenium import webdriver
from bs4 import BeautifulSoup
from nytimesarticle import articleAPI
import string
import os
import time

# Making use of the NYTimes API, you can change the web crawler to your needs here
api = articleAPI('c541b33c45a44c859360c2483c5da811')
page_number = 1
files = 0
articleFileNumber = 38
search_word = 'technology'
while(True):
	if files > 100:
		break
	article = api.search( 
			q = search_word, 
			source = 'The New York Times', 
			begin_date = 20170317,
			page = page_number
		)
	# Get the response from the article object we obtained from the search
	# Then get the documents from the response, the documents contain the article's
	# website URL
	docs_list = article.get('response').get('docs')
	print(len(docs_list))
	# Create a list of all the website URLs relevant to our article search
	try:
		url_list = [doc.get('web_url') for doc in docs_list]
		# Go through the website URLs and collect the content of articles
		for i in range(0, len(url_list)):
			the_url = url_list[i]
			by_directory = [word for word in the_url.split('/') if word.isalpha()]
			if by_directory:
				topic = by_directory[-1]
				articles_seen = set()
				if the_url not in articles_seen:
					content = ""
					response = urlopen(the_url)
					# Get the HTML file of website URL
					html = response.read()
					# Parse the HTML file by turning it into a soup object, makes it pretty
					# and easier to navigate the DOM objects
					soup = BeautifulSoup(html, 'html.parser')
					# Create a txt file in the path(first parameter) with the filename as the
					# title of the article, this will contain the original article content
					# This will help us find all the paragraph tags and make it into one string
					#if topic in topics:
					appended_content = ''
					content = str(soup.find_all('p'))
					paragraphs = []
					for paragraph in content.split('<p'):
						paragraphs.append(''.join(paragraph))
					paragraph_content = [one_paragraph.strip() for one_paragraph in paragraphs if len(one_paragraph) > 1]
					if len(paragraph_content) > 3:
						print(soup.title.string)
						print(topic)
						print(search_word)
						f = open(os.path.join(str(os.getcwd()) + '/Articles/', '{}.txt'.format(str(articleFileNumber))), 'w')
						f.write(''.join(paragraph_content))
						f.close()
						articles_seen.add(the_url)
						articleFileNumber += 1
					else:
						the_unseen.append(the_url)
				time.sleep(1)
		page_number += 1
		print(page_number)
	except:
		page_number += 1
