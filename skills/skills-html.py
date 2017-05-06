#!/bin/env python3

linjer = open("skills.txt", "r").readlines()

skill = {}
skills = [] 

for linje in linjer:
	if not linje.strip():
		skills.append(skill)
		skill = None
		continue
	elif not skill:
		title = linje[0: linje.find("(")].strip()
		id = title.strip().replace(" ", "-").lower()
		category = linje[linje.find("(")+1: -2].lower()
		skill = {'id': id, 'title': title, 'category': category, 'text': ""}
	else:
		skill['text'] = skill['text'] + linje.replace("\n"," ")


for skill in skills:
	print("<article class='{}' id='{}'><h2>{}</h2>{}<p>{}</p></article>".format(skill['category'], skill['id'], skill['title'], skill['category'], skill['text']))
