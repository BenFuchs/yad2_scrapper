import csv
from bs4 import BeautifulSoup
import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
Base = declarative_base()

class Pet(Base):
    __tablename__ = 'pets'
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    location = Column(String)
    price = Column(String)


# Create an SQLite database
engine = create_engine('sqlite:///pets.db')
Base.metadata.create_all(engine)  # Create the table

Session = sessionmaker(bind=engine)
session = Session()

# Fetch the HTML content from the webpage (replace with your URL)
url = 'https://www.yad2.co.il/pets/all?srsltid=AfmBOop_whRhNP2hNDRoZZxfvFUOKIhaLe-G0Mb8nM709JsyEYkW7QoR'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://example.com',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive'
}

response = requests.get(url, headers=headers)
html_content = response.content

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all the feed list items (or relevant divs) that contain the data
feed_list = soup.find_all('div', class_='feeditem')  # Replace with the actual class name for each item

# Loop through each feed item to extract title, location, price, and date
for feed_item in feed_list:
    title = feed_item.find('div', class_='row-1')
    location = feed_item.find('div', class_='val')
    price = feed_item.find('div', class_='price')

    # Get text if the element is found, else set to None
    title_text = title.get_text(strip=True) if title else 'N/A'
    location_text = location.get_text(strip=True) if location else 'N/A'
    price_text = price.get_text(strip=True) if price else 'N/A'


    # Create a new Pet instance
    pet = Pet(title=title_text, location=location_text, price=price_text,)
    
    # Add the instance to the session
    session.add(pet)

# Commit the session to the database
session.commit()

print("Data has been added to the database.")

# Close the session
session.close()
