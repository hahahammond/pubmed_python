# Import libraries
from lxml import html
import requests
import re

# Extract URLs from an individual's Boston University Profile page
page = requests.get('https://profiles.bu.edu/Ali.Guermazi')
tree = html.fromstring(page.content)
urls = tree.xpath('//span/a/@href')

# Initiate PubMed article counter and list
pubmed_url_counter = 0
pubmed_url_list = []

# Find URLs pointing to PubMed articles and add to list
for url in urls:
    pubmed_url = re.findall('//www.ncbi.nlm.nih.gov/pubmed/.*$', url)
    if pubmed_url:
        pubmed_url_list.append(pubmed_url[0])
        pubmed_url_counter += 1
        
# Print number of PubMed articles found and list of their corresponding URLs         
print('\n')
print('Number of PubMed articles: ', pubmed_url_counter)
print('\n')
print('PubMed Article URLs: ', pubmed_url_list)
print('\n')

# Initiate PMID counter
pmid_counter = 0

# Create and open PMID text file
f= open('pmids.txt','w+')

# Find PMIDs in PubMed article URLs and write to text file
for p in pubmed_url_list:
    p2 = p.replace('//www.ncbi.nlm.nih.gov/pubmed/', '')
    print(p2)
    f.write(p2 + '\n')
    pmid_counter += 1

# Close text file
f.close() 

# Print number of PMIDs found
print('\n')
print('Number of PMIDs located: ', pmid_counter)
