from urllib.request import urlopen
from bs4 import BeautifulSoup
import random 
import re
from collections import namedtuple

urlSite = "https://j-archive.com"
pageSite = urlopen(urlSite)

html_bytes_site = pageSite.read()
htmlSite = html_bytes_site.decode("utf-8")

soupSite = BeautifulSoup(htmlSite, 'html.parser')

#print(soupSite.prettify())

seasonsLinksList = []

for linkSite in soupSite.find_all('a'):
	seasonsLinksList.append(linkSite.get('href'))

seasonsLinksList = [x for x in seasonsLinksList if x.startswith('showseason.php')]

random.seed()
seasonNumIndex = random.randint(1,len(seasonsLinksList)) - 1 

print("Season link chosen: " + seasonsLinksList[seasonNumIndex])
#print(seasonsLinksList)

urlSeason = urlSite + "/" + seasonsLinksList[seasonNumIndex]

pageSeason = urlopen(urlSeason)

html_bytes_season = pageSeason.read()
htmlSeason = html_bytes_season.decode("utf-8")

soupSeason = BeautifulSoup(htmlSeason, 'html.parser')

#print(soupSeason.prettify())

episodesLinksList = []

for linkSeason in soupSeason.find_all('a'):
	episodesLinksList.append(linkSeason.get('href'))

episodesLinksList = [x for x in episodesLinksList if "game_id" in x]

random.seed()
episodeNumIndex = random.randint(1,len(episodesLinksList)) - 1 

print("Episode link chosen: " + episodesLinksList[episodeNumIndex])
#print(episodesLinksList)

urlEpisode = episodesLinksList[episodeNumIndex]
pageEpisode = urlopen(urlEpisode)

html_bytes_episode= pageEpisode.read()
htmlEpisode = html_bytes_episode.decode("utf-8")

soupEpisode = BeautifulSoup(htmlEpisode, 'html.parser')
'''
print("---------------------------------------------------------------")
print(soupEpisode.prettify())
print("---------------------------------------------------------------")
'''
soupEpisodeCategories = soupEpisode.find_all("td", {"class": "category_name"})

episodeCategoryNames = [x.text for x in soupEpisodeCategories]

'''
for x in soupEpisodeCategoryNames:
	print(x)
'''

categoryNameIds = {
					episodeCategoryNames[0] : "clue_J_1", 
					episodeCategoryNames[1] : "clue_J_2", 
					episodeCategoryNames[2] : "clue_J_3", 
					episodeCategoryNames[3] : "clue_J_4",
					episodeCategoryNames[4] : "clue_J_5",
					episodeCategoryNames[5] : "clue_J_6",
					episodeCategoryNames[6] : "clue_DJ_1",
					episodeCategoryNames[7] : "clue_DJ_2",
					episodeCategoryNames[8] : "clue_DJ_3",
					episodeCategoryNames[9] : "clue_DJ_4",
					episodeCategoryNames[10] : "clue_DJ_5",
					episodeCategoryNames[11] : "clue_DJ_6",
					episodeCategoryNames[12] : "clue_FJ"
				  }
'''
print("categoryNameIds :")
print("{")
for x in categoryNameIds:
	print(x + " : " + categoryNameIds[x])
print("}")
'''
while True:
	random.seed()
	categoryNameIndex = random.randint(1,len(episodeCategoryNames)-1) - 1 
	chosenCategoryName = episodeCategoryNames[categoryNameIndex]
	print("Chosen category : " + chosenCategoryName + " - Category ID : " + categoryNameIds[chosenCategoryName])

	print("---------------------------------------------------------------")
	clueIds = []
	for x in range(1,6):
		clueIds.append(categoryNameIds[chosenCategoryName] + "_" + str(x))
		
	#print(clueIds)
	#print("---------------------------------------------------------------")

	soupClueTexts = []
	for x in clueIds:
		soupClueText = soupEpisode.find("td", {"class": "clue_text", "id" : x})
		if soupClueText is not None:
			soupClueTexts.append(soupClueText)
		else:
			soupClueTexts.append("")
	#print(soupClueTexts)
	
	if("" not in soupClueTexts):
		break

clueTexts = [x.text for x in soupClueTexts if x != ""]
#print(clueTexts)
#print("---------------------------------------------------------------")
clueAnswers = []
soupClueAnswers = soupEpisode.find_all("div")
for x in soupClueAnswers:
	clueAnswers.append(x.get("onmouseover"))
	
#print(clueAnswers)

clueAnswersText = []
for x in clueIds:
	for y in filter(None,clueAnswers):
		if x in y:
			clueAnswersText.append(re.split('>|<',y.split("em")[1])[1])

#print(clueAnswersText)
#print("---------------------------------------------------------------")
cluesMap = {}
for index, x in enumerate(clueIds):
	clueInfo = {}
	clueInfo['clue'] = clueTexts[index]
	clueInfo['answer'] = clueAnswersText[index]
	cluesMap[x] = clueInfo
#print("---------------------------------------------------------------")
#print(cluesMap)

print("CluesMap : ")
print("{")
for x in cluesMap:
	print("\t" + x + ":")
	print("\t{")
	print("\t\tClue: " + cluesMap[x]['clue'])
	print("\t\tAnswer: " + cluesMap[x]['answer'])
	print("\t}")
print("}")
'''
clueIdsToText = {}
for index, x in enumerate(clueIds):
	clueIdsToText[x] = clueTexts[index]

print("clueIdsToText :")
print("{")
for x in clueIdsToText:
	print(x + " : " + clueIdsToText[x])
print("}")
print("---------------------------------------------------------------")

'''			
