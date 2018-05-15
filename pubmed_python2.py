#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 12 15:57:21 2018

@author: larkink
"""

# Adapted from Biopython tutorial, 9.14  Examples: 9.14.1  PubMed and Medline
# URL: http://biopython.org/DIST/docs/tutorial/Tutorial.html#htoc6
from Bio import Entrez
import matplotlib.pyplot as plt
import operator
import numpy as np
import pandas as pd
from collections import OrderedDict

# In this example, we will query PubMed for all articles having to do with orchids. We first check how many of such articles there are:
Entrez.email = "A.N.Other@example.com"     # Always tell NCBI who you are
handle = Entrez.egquery(term="orchid")
record = Entrez.read(handle)
for row in record["eGQueryResult"]:
    if row["DbName"]=="pubmed":
        print(row["Count"])
        

# Now we use the Bio.Entrez.efetch function to download the PubMed IDs of these articles:
handle = Entrez.esearch(db="pubmed", term="orchid", retmax=463)
record = Entrez.read(handle)
handle.close()
idlist = record["IdList"]

# This returns a Python list containing all of the PubMed IDs of articles related to orchids:
print(idlist)

# Now that we’ve got them, we obviously want to get the corresponding Medline records and extract the information from them. Here, we’ll download the Medline records in the Medline flat-file format, and use the Bio.Medline module to parse them:
from Bio import Medline
handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline", retmode="text")
records = Medline.parse(handle)

# Keep in mind that records is an iterator, so you can iterate through the records only once. If you want to save the records, you can convert them to a list:
records = list(records)

# Let’s now iterate over the records to print out some information about each record:
for record in records:
    print("title:", record.get("TI", "?"))
    print("authors:", record.get("AU", "?"))
    print("source:", record.get("SO", "?"))
    print("")

# Especially interesting to note is the list of authors, which is returned as a standard Python list. This makes it easy to manipulate and search using standard Python tools. For instance, we could loop through a whole bunch of entries searching for a particular author with code like the following:
search_author = "Walker HJ"
for record in records:
    if not "AU" in record:
        continue
    if search_author in record["AU"]:
        print("Author %s found: %s" % (search_author, record["SO"]))

# Kayla's stuff
author_list = []
for record in records:
    if "AU" in record:
        listylist = record.get("AU")
        for a in listylist:
            author_list.append(a)
author_list = sorted(author_list)
for al in author_list:
    print(al)

uniques = set(author_list)
uniques = list(uniques)
uniques = sorted(uniques)
print(uniques)
        
count_dict = dict((el,0) for el in uniques)


for k in count_dict.keys():
    for ab in author_list:
        if k == ab:
            count_dict[k] +=1
print(count_dict)
        

sorted_count_dict = sorted(count_dict.items(), key=operator.itemgetter(1))
sorted_count_dict.reverse()
print(sorted_count_dict)


graph_data = {}
for t,s in count_dict.items():
    if s > 7:
        graph_data[t] = s
print(graph_data)

plt.bar(range(len(graph_data)), list(graph_data.values()), align='center')
plt.xticks(range(len(graph_data)), list(graph_data.keys()))
plt.xticks(rotation=90)
plt.title('Most Citations')
plt.show()

sorted_graph_data = sorted(graph_data.items(), key=operator.itemgetter(1))
sorted_graph_data.reverse()
print(sorted_graph_data)

plt.bar(range(len(sorted_graph_data)), [val[1] for val in sorted_graph_data], align='center')
plt.xticks(range(len(sorted_graph_data)), [val[0] for val in sorted_graph_data])
plt.xticks(rotation=70)
plt.show()



