import json
import time
import datetime
import math
import asyncio
import random
import googletrans
import httpx
from googletrans import Translator

start_time = time.time()

def insert_between(original_list, value_to_insert):
	new_list = []
	for i in range(len(original_list)):
		new_list.append(original_list[i])
		if i < len(original_list) - 1:
			new_list.append(value_to_insert)
	return new_list

with open("config.json", "r") as f:
	config = json.load(f)

with open("translate_list.txt", "r", encoding="utf-8") as f:
	texts_to_translate = f.readlines()

base_language = config["base_language"]
original_language_chain: list[str] = config["language_chain"]
randomize_chain = config["randomize_chain_for_each_string"]
translate_back_to_base = config["translate_back_to_base_each_time"]

translator = Translator()

async def translate(text,from_lang,to_lang) -> str:
	try:
		text_to_translate = await translator.translate(text, src=from_lang, dest=to_lang)
		return text_to_translate.text
	except httpx.LocalProtocolError as e:
		print(f"Failed to translate '{text}': from {from_lang} to {to_lang}")

	return text

async def main():
	all_final_translations = []
	for text in texts_to_translate:
		ft = await chain_translate(text)
		all_final_translations.append(ft)

	print("FINISHED! Here are all the final translations:")
	print()
	for ft in all_final_translations:
		print(ft)
	print()

	t = time.localtime()
	current_time = time.strftime("%H:%M:%S", t)

	end_time = time.time()
	elapsed_time_seconds = end_time - start_time
	elapsed_time_seconds_truncated = math.trunc(elapsed_time_seconds)

	elapsed_time = datetime.timedelta(seconds=elapsed_time_seconds_truncated)

	print("Translations completed at:", current_time)
	print("Elapsed time:", str(elapsed_time).zfill(8))

	# newChain = ""
	# for i in language_chain:
	#   newChain+='"'
	#	 newChain+=i
	#	 newChain+="\","
	# print(newChain)

async def chain_translate(text_to_translate: str):
	language_chain = original_language_chain.copy()
	print("Total Languages: ", len(language_chain))
	if randomize_chain:
		random.shuffle(language_chain)
	if translate_back_to_base:
		language_chain = insert_between(language_chain, base_language)
	language_chain.insert(0, base_language)
	print(language_chain)
	# language_chain = ["zh","pa","vi","yi","haw","sl","fr","ro","mn","el","pt","es","ja","ne","pl","it","is","da","he","nl","am","ar","ru","tl","ko","sv","uk","de","fi","hi","cy","zu"]#["es","de","fr","zh","da","el","por","ru","he","ja","fi","ko","is","it","vi","ar","sv","uk","haw","ro","pl","ne","sl","hi","yi","zu","cy","pa","mn","tl","nl"]
	# language_chain.sort()
	starting_message = text_to_translate
	current_message = starting_message
	print("Starting Message: ", current_message)

	for i in range(len(language_chain) - 1):
		cur_lang = language_chain[i]
		next_lang = language_chain[i+1]
		current_message = await translate(current_message, cur_lang, next_lang)

		if translate_back_to_base:
			if next_lang == base_language:
				print(cur_lang, "->", next_lang, " | ", current_message)
		else:
			print(next_lang, " | ", current_message)

	current_message = await translate(current_message, language_chain[-1], language_chain[0])

	if translate_back_to_base:
		print("Final Translation: ", language_chain[-1], "->", language_chain[0], " | ", current_message)
	else:
		print("Final Translation: ", current_message)

	print("-------------------------------------------------------------")
	return current_message

if config["print_all_available_languages"]:
	print("Printing all available languages:")
	for k,v in googletrans.LANGUAGES.items():
		print(k,v)
	print("All available languages ^^^")
	print("----------------------------------------------------")
	print("NOTICE!")
	print("We have deliberately skipped doing any translations.")
	print("If you want to do translations, please set the 'print_all_available_languages' string to false in the config.")
	print("This is a separate mode to allow you to see all languages and pick what you want for your chains.")
else:
	asyncio.run(main())
