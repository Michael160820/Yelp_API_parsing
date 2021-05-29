import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://api.yelp.com/v3/businesses/search?categories=vegan&cafe&Restaurants&location=San Francisco, CA&radius=10000&limit=50'
API_KEY = '3PDfUGAj_aphNHC-11RO51GE1oTTO5LTz7SkKIBa4oSVcObXbtwPp86H_SKypMnJJzeLSmvVqS_G2UhW1OV0hI8D1MgWpXoqbhAlfHtRoibtna-Ed_RmZ02Jf5sNYHYx'

if __name__ == '__main__':
    headers = {'Authorization': 'Bearer ' + API_KEY}
    request = requests.get(BASE_URL, headers=headers)
    if request.status_code != 200:
        raise ValueError(f'Status code = {request.status_code}')

    cafes = request.json()

    for cafe in cafes['businesses']:
        url = cafe['url']
        request = requests.get(url)

        print('name: ', cafe['name'])
        print('phone: ', cafe['phone'])
        print('website: ', cafe['url'])
        print('tags: ', [i['alias'] for i in cafe['categories']])
        print('address: ', cafe['location']['address1'] )
        print('city: ', cafe['location']['city'])
        print('zip-code: ', cafe['location']['zip_code'])
        print('latitude: ', cafe['coordinates']['latitude'])
        print('longitude: ', cafe['coordinates']['longitude'])
        print('rating: ', cafe['rating'])
        url_google='https://www.google.com/search?q=' + (cafe['name']).replace(' ', '+') + (cafe['location']['city']).replace(' ', '+')
        print('по этой ссылке планировал найти адрес сайта и рейтинг google ' + url_google)
        r = requests.get('https://www.google.com/search?q=' + (cafe['name']).replace(' ', '+') + (cafe['location']['city']).replace(' ', '+'))
        soup = BeautifulSoup(r.text, 'html.parser')
        mains = soup.find_all('div', {'class': 'xpdopen'})
        for main in mains:
            try:
                site_adr = main.find('a', {'class': 'ab_button'}).get('href')
                google_rate = main.find('span', {'class': 'Aq14fc'}).text
                print('website: ' + site_adr)
                print('google rate: ' + google_rate)
            except:
                print(None)
        print('______'*20)
