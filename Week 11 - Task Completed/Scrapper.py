import requests
from bs4 import BeautifulSoup

car =input("Enter manufacturer name:")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://google.com"
}
url=f'https://www.pakwheels.com/new-cars/pricelist/{car}'

response=requests.get(url, headers=headers)

if response.status_code == 200:
    soup=BeautifulSoup(response.text,'html.parser')
    tables=soup.find_all('table')
    for table in tables:
        rows=table.find_all('tr')
        for row in rows:
            cols=row.find_all('td')
            if len(cols)>=2:
                name=cols[0].get_text()
                price=cols[1].get_text()
                print(f"Car Name: {name} - Price: {price}")
        
        
        
    
    
    
    
    
    
    
else:
    print("Page not available !")

# function to save data on csv file
def save_to_csv(data, filename):
    pass







