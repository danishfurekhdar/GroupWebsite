import requests
from bs4 import BeautifulSoup
import json
import platform

session = requests.Session()
# Replace 'YOUR_GOOGLE_SCHOLAR_URL' with the actual URL to your Google Scholar profile.
url = 'https://scholar.google.de/citations?hl=de&user=cyQLH48AAAAJ&view_op=list_works&sortby=pubdate'

# Define user-agent headers for different platforms
user_agents = {
    'Linux': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Windows': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Darwin': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# Get the current platform
current_platform = platform.system()

# Select the appropriate user-agent based on the platform
user_agent = user_agents.get(current_platform, user_agents['Linux'])

# Create headers with the selected user-agent
headers = {
    'User-Agent': user_agent
}


# Send an HTTP GET request to the Google Scholar profile page with the User-Agent header.
response = session.get(url, headers=headers)

# Check if the request was successful (status code 200).
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the publication elements on the page.
    publication_elements = soup.find_all('tr', {'class': 'gsc_a_tr'})

    # Extract publication data.
    publication_data = []
    for pub_element in publication_elements:
        title = pub_element.find('a', {'class': 'gsc_a_at'}).text
        authors = pub_element.find('div', {'class': 'gs_gray'}).text
        publication_year = pub_element.find('span', {'class': 'gsc_a_h gsc_a_hc gs_ibl'}).text
        
        # Find the publication link, if available
        source_link_element = pub_element.find('a', {'class': 'gsc_a_at'})
        source_link = source_link_element['href'] if source_link_element else 'Link Not Found'
        
        # Ensure the source link includes "https://scholar.google.de/"
        if not source_link.startswith('https://scholar.google.de/'):
            source_link = 'https://scholar.google.de' + source_link
        
        # Initialize DOI as 'DOI Not Found'
        doi = 'DOI Not Found'
        
        # Send a request to the publication page
        publication_page = session.get(source_link, headers=headers)
        
        # Check if the request was successful (status code 200)
        if publication_page.status_code == 200:
            publication_soup = BeautifulSoup(publication_page.text, 'html.parser')
            
            # Find the publication title link on the publication page
            title_link_element = publication_soup.find('a', {'class': 'gsc_oci_title_link'})
            
            if title_link_element:
                title_link = title_link_element['href']
                doi = title_link
                        
        # Add more fields as needed
        
        publication_info = {
            'title': title,
            'authors': authors,
            'year': publication_year,
            'link': doi,  # Include the DOI in the publication info
            # Add more fields as needed
        }
        publication_data.append(publication_info)

    # Store the publication data in a JSON file.
    with open('publications.json', 'w', encoding='utf-8') as file:
        json.dump(publication_data, file, ensure_ascii=False, indent=4)

    print('Publication data scraped and saved to publications.json')
else:
    print('Failed to retrieve data. Check your URL or internet connection.')
