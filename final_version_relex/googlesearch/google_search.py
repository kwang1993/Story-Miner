from bs4 import BeautifulSoup
import mechanize
from copy import copy
import time
from random import random

def google_search(topic_words,output_file):
	#words = ["magma","terrane", "volcano", "uplift", "eruptions", "arc", "plateau", "terranes", "paleozoic", "emplacement"]
	#words = ["nitride", "sic", "diamond", "tunable", "gaas", "glasses", "fuel", "ferroelectric", "nanotubes", "arsenide"]
	
	##words = ["","","bill", "senate", "senator", "president", "congress", "committee", "fax", "bush", "bills", "nj"]
	#words = ["","","malaria", "traveling", "travelling", "mexico", "yellow", "rica", "costa", "plane", "travel", "mosquito"]
	words = ["",""]
	for w in topic_words:
		words.append(w)
	
	num_words = len(words)

#	fw = open("output/mothering_th26_topic2_eval_2.csv", mode='w')
	fw = open(output_file, mode='w')
	fw.write(",,," + ",".join(words) + '\n')

	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.set_handle_equiv(False)
	br.addheaders = [('User-agent', 'Mozilla/16.0')] 

	search_combs = set()
	
	counter = 1
	for i in range(0,num_words):
		for j in range(i+1,num_words):
			for k in range(j+1,num_words):

				word1 = words[i]
				word2 = words[j]
				word3 = words[k]				

				query_string = word1 + ' ' + word2 + ' ' + word3
				
				if query_string not in search_combs:
					search_combs.add(query_string)
					
					other_words = copy(words)
					other_words.remove(word1)
					other_words.remove(word2)
					other_words.remove(word3)
					br.open('http://www.google.com/')   

					# do the query
					br.select_form(name='f')
					br.form['q'] = query_string # query
					data = br.submit()
					html_source = data.read()

					hits = [0]*len(words)
					hits[i] = (word1 in html_source)*1
					hits[j] = (word2 in html_source)*1
					hits[k] = (word3 in html_source)*1

					for word in other_words:
						ind = words.index(word)
						hits[ind] = (word in html_source)*1
						


					fw.write(query_string.replace(' ',',') + ',' + str(hits)[1:-1] + '\n')
					
					print (output_file + '\t' + str(counter))
					
					counter += 1
					
					if (counter % 50) == 0:
						time.sleep(60 + random()*10)
					
					time.sleep(3 + random()*3)


	fw.close()

	#result_divs = soup.findAll('div', class= "rc")
