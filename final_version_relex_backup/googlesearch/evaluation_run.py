from google_search import google_search
import sys

#evaluation_file = "/media/data1/misagh/Cooccurrence_Network/evaluation_scripts/wiki_results/NSF_topics_th46_eval.txt"
topics_file = '/media/data1/misagh/Cooccurrence_Network/Cooccurrence_Network_Zicong/Cooccurrence_Network/Reuters/Reuters_LDA_100_topics.txt'

topics = []
with open(topics_file) as f:
	line = f.readline()
	while (len(line)!=0):
		if line.startswith("Topic "):
			topic_words = line.strip('\n').split(": ")[1].split(" ")
			topic_words = topic_words[0:10]
			topics.append(topic_words)
			print topic_words
		line = f.readline()
		

for i in range(0,len(topics)):
	search_done = False
	count = 0
	while ((search_done==False) and (count<10)):
		try:
			google_search(topics[i],"Reuters_LDA_google/Reuters_LDA_topic" + str (i+1) + ".csv")
			search_done = True
		except:
			search_done = False
			count += 1
		if count==10:
			sys.exit("error: could not complete search")
			

