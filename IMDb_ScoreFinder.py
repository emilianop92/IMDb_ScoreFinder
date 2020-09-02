import json
import requests
from bs4 import BeautifulSoup
import re


api = 'http://www.omdbapi.com/'
key = '142a4256'


def ratingsSearch(website, domain):

	html = requests.get(website)
	soup = BeautifulSoup(html.text, 'html.parser')
	
	if domain in ['nytimes', 'digitaltrends', 'wired.co', 'thrillist']:
		movies_soup = soup.find_all('h2')
	elif domain in ['esquire', 'townandcountrymag']:
		movies_soup = soup.find_all('span', {'class':'listicle-slide-hed-text'})
	else:
		print('Sorry, I do not support that domain yet, but I will try!')
		movies_soup = soup.find_all('h2')

	all_movies = []
	regex = r'\(\d\d\d\d\)'

	for movie in movies_soup:
		print(movie)
		movie = movie.text.strip()
		has_year = re.search(regex, movie) != None
		
		if has_year:
			title = ' '.join(movie.split()[:-1])
			if domain == 'nytimes':
				title = title[1:-1]
		else:
			title = movie

		api_search = api+'?t='+title+'&apikey='+key
		json_data = requests.get(api_search)

		try:
			year = json.loads(json_data.text)['Year']
			rating = json.loads(json_data.text)['imdbRating']
			plot = json.loads(json_data.text)['Plot']
			all_movies.append([title, year, rating, plot])
			print('Found a rating...')
		except:
			print('Exception!')
			pass

	return all_movies