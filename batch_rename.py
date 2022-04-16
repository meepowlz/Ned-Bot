# tfw u just do not want to type that out

import os

directory = r"C:\Users\Meep\Desktop\DOOM Eternal Original Game Soundtrack (OST 2020)\\"

def do_it(directory):

	for i, file_name in enumerate(os.listdir(directory)):

		old_name = directory + file_name

		new_name = directory + file_name[5:len(file_name)]
		os.rename(old_name, new_name)

	for file_name in os.listdir(directory):
		print(file_name)

