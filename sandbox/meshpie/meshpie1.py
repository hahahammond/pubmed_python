# Import libraries
import lxml.html
import requests
import re
import pandas as pd
import matplotlib.pyplot as plt
from pandas.tools.plotting import table
import seaborn as sns
import numpy as np
import io
import base64
import urllib.parse

# Create empty df for MeSH terms data
mesh_tally_cols = ['Term','Frequency', 'URL']
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
        if (mesh_tally.Term == term).any():
            mesh_tally.loc[mesh_tally.Term == term, 'Frequency'] += 1
        if not (mesh_tally.Term == term).any():
            mesh_tally_dict = {}
            mesh_tally_dict['Term'] = term
            mesh_tally_dict['Frequency'] = 1
            if len(term.split()) > 1:
                plussed_term = term.replace(" ", "+")
                mesh_tally_dict['URL'] = 'https://www.ncbi.nlm.nih.gov/mesh?term=' + plussed_term
            else:
                mesh_tally_dict['URL'] =  'https://www.ncbi.nlm.nih.gov/mesh?term=' + term  
            mesh_tally = mesh_tally.append(mesh_tally_dict, ignore_index=True)
            mesh_tally['Frequency'] = mesh_tally['Frequency'].astype(int)
    
mesh_tally.to_csv('mesh_tally.csv', index=False)
        
print(mesh_tally)

with pd.option_context('display.max_colwidth', -1): 
    table = mesh_tally.to_html(index=False).replace('<table','<table class="table-striped table-bordered dt-responsive nowrap" id="results" style="width:100%;"')

with open("output1.html", "w") as file:
    file.write(str(table))
    
# Create pie chart with top MeSH terms by frequency

mesh_tally['Frequency'].plot(kind='pie', subplots=True) 
plt.show()

mesh_tally['Frequency'].plot(kind='pie', labels=mesh_tally['Term'], autopct='%.2f', fontsize=20)
plt.show()

top_mesh_tally =  mesh_tally.nlargest(10, 'Frequency')

top_mesh_tally['Frequency'].plot(
        kind='pie', 
        labels=top_mesh_tally['Term'], 
        fontsize=10, 
        title= "Top Ten MeSH Terms")
plt.show()


# Create bar chart

vert_fig = sns.barplot(top_mesh_tally['Term'], top_mesh_tally['Frequency'], alpha=0.8,  palette="Blues_d")
plt.title('Top Ten MeSH Terms')
plt.ylabel('Frequency', fontsize=12)
plt.xlabel('MeSH Term', fontsize=12)
plt.xticks(rotation=90)
plt.show(vert_fig)

horiz_fig = sns.barplot(top_mesh_tally['Frequency'], top_mesh_tally['Term'], palette="pastel")
plt.title('Top Ten MeSH Terms')
plt.ylabel('MeSH Term', fontsize=12)
plt.xlabel('Frequency', fontsize=12)
plt.show(horiz_fig)


img = io.BytesIO()  # create the buffer
sns.barplot(top_mesh_tally['Frequency'], top_mesh_tally['Term'], palette="pastel")
plt.title('Top Ten MeSH Terms')
plt.ylabel('MeSH Term', fontsize=12)
plt.xlabel('Frequency', fontsize=12)

plt.savefig(img, format='png')  # save figure to the buffer
img.seek(0)  # rewind your buffer
plot_data = urllib.parse.quote(base64.b64encode(img.read()).decode()) # base64 encode & URL-escape
#return render_template('plot.html', plot_url=plot_data)

