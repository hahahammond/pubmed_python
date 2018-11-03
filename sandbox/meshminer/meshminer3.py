# Import libraries
import os
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import lxml.html
import requests
import re
import pandas as pd


# Import libraries
import operator

# Create empty dictionary for MeSH terms
mesh_tally = {}


# Create PMID list

# FROM TXT FILE
with open('epilepsy.txt', 'r') as input_file: 
    pmid_str=input_file.read().replace('\n', ' ')

# FROM STR
#pmid_str = "30170574, 30130317, 30115126, 30089083, 30088578, 30046807, 29999103, 29966882, 29927272, 29902142"

pmid_list = re.findall(r'\d+', pmid_str)
print("PMID List: ", pmid_list)

for pmid in pmid_list:
    # Assemble URLs for articles
    url = 'https://www.ncbi.nlm.nih.gov/pubmed/' + str(pmid)
    print(url)
    
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
        if term in mesh_tally.keys():
            mesh_tally[term] += 1
        else:
            mesh_tally[term] = 1

# Sort mesh_tally dictionary by value in ascending order
sorted_mesh_tally = sorted(mesh_tally.items(), key=lambda x: (x[1],x[0]), reverse=True)

print(sorted_mesh_tally)

# Create output dataframe
output_columns = ['MeSH Term', 'Frequency']
output_df = pd.DataFrame(data=sorted_mesh_tally, columns=output_columns)
print(output_df.head())

# Create output CSV
output_df.to_csv("output.csv", index=False)

