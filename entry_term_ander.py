# Entry Term AND-er

# Import libraries
import lxml.html
import requests
import re

# Create and open Entry Term text file
f= open('entry_terms.txt','w+')

# Enter URL from MeSH page 
url = '[ENTER URL FOR MESH TERM HERE]'

# Remove ezproxy from URL if necessary
ezproxy = 'https://www-ncbi-nlm-nih-gov.ezproxy.bu.edu/'
no_ezproxy = 'https://www.ncbi.nlm.nih.gov/'

if ezproxy in url:
    url = url.replace(ezproxy, no_ezproxy)

# Make request
r = requests.get(url)

# Find and print MeSH Heading
root = html.fromstring(r.content)
mesh = root.xpath('//h1/text()')
clean_mesh = mesh[0].replace("'", "")
print('MeSH Heading:')
print(clean_mesh)
print('\n')


# Find and print Entry Terms
entry_terms = root.xpath('//li/text()')

print('Entry terms:')
for entry_term in entry_terms:
    print(entry_term)
print('\n')

# Count and print number of Entry Terms
entry_term_counter = 0

for entry_term in entry_terms:
    entry_term_counter += 1
    
print('Number of Entry Terms located: ')
print(entry_term_counter)
print('\n')

# Write MeSH Heading to text file
print('"' + clean_mesh + '"[Mesh]')
f.write('"' + clean_mesh + '"[Mesh]')

# Write all remaining Entry Terms to text file, separated by OR
for entry_term in entry_terms[1:]:
    clean_entry_term = entry_term.replace("'", "")
    print(' OR ' + clean_entry_term)
    f.write(' OR ' + clean_entry_term)
    
# Close text file
f.close()    
    