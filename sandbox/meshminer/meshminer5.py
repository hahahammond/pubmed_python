# Import libraries
import lxml.html
import requests
import re
import pandas as pd

# Create empty df for MeSH terms data
mesh_tally_cols = ['raw_term', 'Frequency', 'URL', 'Term']
mesh_tally = pd.DataFrame(columns = mesh_tally_cols)

pmid_str = "30170574, 30130317, 30115126, 30089083, 30088578, 30046807, 29999103, 29966882, 29927272, 29902142"

pmid_list = re.findall(r'\d+', pmid_str)

for pmid in pmid_list:
    # Assemble URLs for articles
    url = 'https://www.ncbi.nlm.nih.gov/pubmed/' + str(pmid)

    # Make request
    r = requests.get(url)
    root = lxml.html.fromstring(r.content)

    # Find MeSH terms
    mesh_terms = root.xpath('//li/a[@alsec="mesh"]/text()')
    for term in mesh_terms:
        if '/' in term:
            term = term.rsplit('/')[0]
        if '*' in term:
            term = term.rsplit('*')[0]
        if (mesh_tally.raw_term == term).any():
            mesh_tally.loc[mesh_tally.raw_term == term, 'Frequency'] += 1
        if not (mesh_tally.raw_term == term).any():
            mesh_tally_dict = {}
            mesh_tally_dict['raw_term'] = term
            mesh_tally_dict['Frequency'] = 1
            if len(term.split()) > 1:
                plussed_term = term.replace(" ", "+")
                mesh_tally_dict['URL'] = 'https://www.ncbi.nlm.nih.gov/mesh?term=' + plussed_term
            else:
                mesh_tally_dict['URL'] =  'https://www.ncbi.nlm.nih.gov/mesh?term=' + term  
            mesh_tally_dict['Term'] = "<a href='" + mesh_tally_dict["URL"] + "'>" + mesh_tally_dict['raw_term'] + "</a>"
            mesh_tally = mesh_tally.append(mesh_tally_dict, ignore_index=True)
            mesh_tally2 = mesh_tally[['Term','Frequency']].copy()
    
mesh_tally2.to_csv('mesh_tally2.csv', index=False)
        
print(mesh_tally2)