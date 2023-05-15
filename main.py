# The dummy function are there only to prevent the sections comments and the funtion comments to collapse
# on each other to keep visibility and readability.
#
# This software aims to scrape whatever website is selected for torrents based either on a keyword or a category
# and displays it in a treeview where it can be selected and either opened or downloaded automatically on qBitorrent.
#
# DON'T FORGET TO LOGIN TO QBITORRENT FROM THE MENU!!!!!
#
# You can select a bunch of settings from the menus, including the website where to search torrents from, the amount
# of results wanted, the language for the subtitles that you might want to search and so on.
#
# If a movie or TV Show episode is downloaded it opens a subtitles windows that will search OpenSubtitles for that
# movie's subtitles based on the language defined in the settings menu.
#
# DON'T FORGET TO LOGIN TO OPEN SUBTITLES FROM THE MENU!!!!!
#
# You can also search for and download subtitles independent of the need to download the movie from a torrent
# from the menu "Search for Subtitles".
def dummy_funtion():
	pass


# -----------------------------------------Imports Section-----------------------------------------
import datetime, re, random, requests, urllib3, qbittorrentapi, json, os, base64

import tkinter as tk
import customtkinter as ctk

from bs4 import BeautifulSoup

from tkinter import ttk, Menu, END, messagebox, filedialog
from tkinter.messagebox import askyesno

from customtkinter import *

from CTkMessagebox import CTkMessagebox

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchWindowException

from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File

# -----------------------------------------Disable Warnings from Websites-----------------------------------------
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# -----------------------------------------Global Variables Initialization-----------------------------------------
search_history_file = "search_history.json"
credentials_file = "credentials.json"
settings_file = "settings.json"

login_qbit_status = "False"
login_ost_status = "False"
ost = OpenSubtitles()
subtitles = []
driver = None

user_agents = [
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.3",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
]


# ---------------------------------------Torrents Search and Display Functions---------------------------------------
def dummy_funtion():
	pass


# On Torrent Search Button Click Function
def search_button_click(mode, query, title):
	if site_url == "https://1337x.unblockit.asia/":
		search_1337x(mode, "search/" + query, title)
	elif site_url == "https://torrentgalaxy.mx/":
		search_torrent_galaxy(mode, query, title)
	elif site_url == "https://solidtorrents.to/":
		search_solidtorrents(mode, query, title)


# Search for Torrents on the 1337x WebSite
def search_1337x(mode, query, title=None):
	global results_count, desired_results, site_url, user_agents
	
	base_url = site_url
	results = []
	results_count = 0
	
	headers = {"User-Agent": random.choice(user_agents)}
	
	if mode == "category":
		search_url = f"{base_url}{query}"
		r = requests.get(search_url, headers=headers, verify=False)
		soup = BeautifulSoup(r.text, "html.parser")
		result_table = soup.find("table", class_="table-list table table-responsive table-striped")
		result_rows = result_table.find_all("tr")
		
		for row in result_rows[1:]:
			name = row.find("td", class_="coll-1 name").find("a").text.strip()
			
			seeds = row.find("td", class_="seeds").text.strip()
			
			input_str = row.find("td", class_="coll-4").text.strip()
			split_str = input_str.split('B')
			size = split_str[0] + 'B'
			
			uploader = row.find("td", class_="coll-5").text.strip()
			
			url = find_url(row)
			
			# icon_link = row.find("a", class_="icon")
			# sub_section = icon_link["href"].split("/")[2]
			category = "sub_section"
			if category == "4" or category == "42" or category == "54" or category == "70" or category == "73" or category == "76":
				category = "Movies"
			
			results.append((name, seeds, size, uploader, url, category))
	
	elif mode == "keyword":
		for pagenumber in range(1, desired_results):
			search_url = f"{base_url}{query}/{pagenumber}/"
			r = requests.get(search_url, headers=headers, verify=False)
			soup = BeautifulSoup(r.text, "html.parser")
			result_table = soup.find("table", class_="table-list table table-responsive table-striped")
			result_rows = result_table.find_all("tr")
			
			for row in result_rows[1:]:
				name = row.find("td", class_="coll-1 name").text.strip()
				
				seeds = row.find("td", class_="seeds").text.strip()
				
				input_str = row.find("td", class_="coll-4").text.strip()
				split_str = input_str.split('B')
				size = split_str[0] + 'B'
				
				uploader = row.find("td", class_="coll-5").text.strip()
				
				url_element = base_url
				url = find_url(row)
				# url = url[0:]
				url = url_element + url[1:]
				
				icon_link = row.find("a", class_="icon")
				sub_section = icon_link["href"].split("/")[2]
				category = sub_section
				if category == "4" or category == "42" or category == "54" or category == "70" or category == "73" or category == "76":
					category = "Movies"
				else:
					category = ""
				
				results.append((name, seeds, size, uploader, url, category))
		
		query = query.replace("search/", "")
		save_search_history(query, search_history_menu)
	
	elif mode == "keyword2":
		for pagenumber in range(1, desired_results):
			search_url = f"{base_url}{query}/{pagenumber}/"
			r = requests.get(search_url, headers=headers, verify=False)
			soup = BeautifulSoup(r.text, "html.parser")
			result_table = soup.find("table", class_="table-list table table-responsive table-striped")
			result_rows = result_table.find_all("tr")
			
			for row in result_rows[1:]:
				name = row.find("td", class_="coll-1 name").text.strip()
				
				seeds = row.find("td", class_="seeds").text.strip()
				
				input_str = row.find("td", class_="coll-4").text.strip()
				split_str = input_str.split('B')
				size = split_str[0] + 'B'
				
				uploader = row.find("td", class_="coll-5").text.strip()
				
				url_element = base_url
				url = find_url(row)
				# url = url[0:]
				url = url_element + url[1:]
				
				icon_link = row.find("a", class_="icon")
				sub_section = icon_link["href"].split("/")[2]
				category = sub_section
				if category == "4" or category == "42" or category == "54" or category == "70" or category == "73" or category == "76":
					category = "Movies"
				else:
					category = ""
				
				results.append((name, seeds, size, uploader, url, category))
	
	query = query.replace("search/", "")
	website = "1337x"
	torrent_treeview_insertion(website, results, query, title, mode)


# Search for Torrents on the Torrent Galaxy WebSite
def search_torrent_galaxy(mode, query, title=None):
	global results_count, desired_tgx_results, site_url, user_agents
	
	base_url = site_url
	results = []
	
	headers = {"User-Agent": random.choice(user_agents)}
	
	if mode == "category":
		search_url = f"{base_url}torrents.php?{query}"
		r = requests.get(search_url, headers=headers, verify=False)
		soup = BeautifulSoup(r.text, "html.parser")
		result_table = soup.find("div", class_="tgxtable")
		result_rows = result_table.find_all("div", class_="tgxtablerow")
		
		for row in result_rows:
			name = row.find("div", class_="clickable-row").text.strip()
			
			seeds = row.find("span", title="Seeders/Leechers").text.strip()
			seeds = seeds.split("/")[0]
			seeds = seeds.replace("[", "")
			seeds = seeds.replace(",", "")
			
			size = row.find("span", class_="badge badge-secondary").text.strip()
			
			uploader = row.find("span", class_="username").text.strip()
			
			url = find_url(row)
			url = site_url + url
			
			category = row.find_all("div", class_="tgxtablecell")[0].text.strip()
			category = category.split(":")[0]
			if category == "Movies" or category == "TV":
				category = "Movies"
			
			results.append((name, seeds, size, uploader, url, category))
	
	elif mode == "keyword":
		for pagenumber in range(0, desired_tgx_results):
			search_url = f"{base_url}torrents.php?search={query}&sort=id&order=desc&page={pagenumber}"
			r = requests.get(search_url, headers=headers, verify=False)
			soup = BeautifulSoup(r.text, "html.parser")
			result_table = soup.find("div", class_="tgxtable")
			result_rows = result_table.find_all("div", class_="tgxtablerow")
			
			for row in result_rows:
				name = row.find("div", class_="clickable-row").text.strip()
				
				seeds = row.find("span", title="Seeders/Leechers").text.strip()
				seeds = seeds.split("/")[0]
				seeds = seeds.replace("[", "")
				seeds = seeds.replace(",", "")
				
				size = row.find("span", class_="badge badge-secondary").text.strip()
				
				uploader = row.find("span", class_="username").text.strip()
				
				url = find_url(row)
				url = site_url + url
				
				category = row.find_all("div", class_="tgxtablecell")[0].text.strip()
				category = category.split(":")[0]
				if category == "Movies" or category == "TV":
					category = "Movies"
				
				results.append((name, seeds, size, uploader, url, category))
	
	website = "Torrent Galaxy"
	torrent_treeview_insertion(website, results, query, title, mode)


# Search for Torrents on the SolidTorrents WebSite
def search_solidtorrents(mode, query, title=None):
	global results_count, desired_solidtorrents_results, site_url, user_agents
	
	headers = {"User-Agent": random.choice(user_agents)}
	base_url = site_url
	results = []
	
	if mode == "category":
		for pagenumber in range(1, desired_solidtorrents_results):
			search_url = f"{base_url}{query}&page={pagenumber}"
			r = requests.get(search_url, headers=headers, verify=False)
			soup = BeautifulSoup(r.text, "html.parser")
			result_table = soup.find("div", class_="w3-col s12 mt-1")
			result_rows = result_table.find_all("li", class_="card search-result my-2")
			
			for row in result_rows:
				name = row.find("h5", class_="title w-100 truncate").text.strip()
				
				seeds = row.find("font", color="#0AB49A")
				seeds = convert_seeds_value(seeds.text.strip()) if seeds else 0
				
				size = row.find("img", alt="Size").find_parent("div")
				size = size.text.strip() if size else ""
				
				uploader = ""
				
				# magnet_link = row.find("a", class_="dl-magnet")
				# magnet_link = magnet_link["href"] if magnet_link else ""
				
				url = row.find("h5", class_="title w-100 truncate").find("a")
				url = url["href"] if url else ""
				url = url[1:]
				url = site_url + url
				
				category = row.find_all("a", class_="category")[0].text.strip()
				if category == "Movies" or category == "TV" or category == "Other/Video":
					category = "Movies"
				
				results.append((name, seeds, size, uploader, url, category))
	
	elif mode == "keyword":
		for pagenumber in range(1, desired_solidtorrents_results):
			search_url = f"{base_url}search?q={query}&page={pagenumber}"
			r = requests.get(search_url, headers=headers, verify=False)
			soup = BeautifulSoup(r.text, "html.parser")
			result_table = soup.find("div", class_="w3-col s12 mt-1")
			result_rows = result_table.find_all("li", class_="card search-result my-2")
			
			for row in result_rows:
				name = row.find("h5", class_="title w-100 truncate").text.strip()
				
				seeds = row.find("font", color="#0AB49A")
				seeds = convert_seeds_value(seeds.text.strip()) if seeds else 0
				
				size = row.find("img", alt="Size").find_parent("div")
				size = size.text.strip() if size else ""
				
				uploader = ""
				
				# magnet_link = row.find("a", class_="dl-magnet")
				# magnet_link = magnet_link["href"] if magnet_link else ""
				
				url = row.find("h5", class_="title w-100 truncate").find("a")
				url = url["href"] if url else ""
				url = url[1:]
				url = site_url + url
				
				category = row.find_all("a", class_="category")[0].text.strip()
				if category == "Movies" or category == "TV" or category == "Other/Video":
					category = "Movies"
				
				results.append((name, seeds, size, uploader, url, category))
	
	elif mode == "top100":
		search_url = f"{base_url}{query}"
		r = requests.get(search_url, headers=headers, verify=False)
		soup = BeautifulSoup(r.text, "html.parser")
		result_table = soup.find("div", class_="w3-col s12 mt-0")
		result_rows = result_table.find_all("div", class_="info px-3 pt-2 pb-3")
		
		for row in result_rows:
			name = row.find("h5", class_="title w-100 truncate").text.strip()
			
			seeds = row.find("font", color="#0AB49A")
			seeds = convert_seeds_value(seeds.text.strip()) if seeds else 0
			
			size = row.find("img", alt="Size").find_parent("div")
			size = size.text.strip() if size else ""
			
			uploader = ""
			
			# magnet_link = row.find("a", class_="dl-magnet")
			# magnet_link = magnet_link["href"] if magnet_link else ""
			
			url = row.find("h5", class_="title w-100 truncate").find("a")
			url = url["href"] if url else ""
			url = url[1:]
			url = site_url + url
			
			category = row.find_all("a", class_="category")[0].text.strip()
			if category == "Movies" or category == "TV" or category == "Other/Video":
				category = "Movies"
			
			results.append((name, seeds, size, uploader, url, category))
	
	website = "Solid Torrents"
	torrent_treeview_insertion(website, results, query, title, mode)


# Inserts all the Values retrieved from the Websites into the Treeview
def torrent_treeview_insertion(website, results, query, title, mode):
	if not query:
		return
	results_count = 0
	tree.delete(*tree.get_children())
	for result in results:
		tree.insert("", "end", values=result)
		results_count += 1
	
	display_title = title if mode == "category" else query
	
	root.geometry("700x490")
	root.title(f"Torrent Finder - Searching for _{display_title}_ on {website} - {results_count} results.")


# Searches for Torrents using a Keyword from History
def history_search(history_keyword):
	if site_url == "https://1337x.unblockit.asia/":
		search_1337x("keyword", history_keyword, history_keyword)
	elif site_url == "https://torrentgalaxy.mx/":
		search_torrent_galaxy("keyword", history_keyword, history_keyword)
	elif site_url == "https://solidtorrents.to/":
		search_solidtorrents("keyword", history_keyword, history_keyword)
	
	history_keyword = history_keyword.replace("search/", "")
	
	keyword_entry.delete(0, END)
	keyword_entry.insert(0, history_keyword)


# -----------------------------------------Torrents Helper Functions-----------------------------------------
def dummy_funtion():
	pass


# Finds the Torrent URL so that it can be later used to retrieve the Magnet Link
def find_url(row):
	anchor_tag = row.find("a", href=lambda href: href and "torrent/" in href)
	if anchor_tag:
		torrent_url = anchor_tag["href"]
	return torrent_url


# Gets Torrents Magnet Link then opens the Magnet Link on qBitorrent and starts the Download
def download_torrent():
	global site_url, subtitles_listbox
	
	download_status.set(0)
	
	selected_item = tree.selection()[0]
	item_data = tree.item(selected_item)
	download_status.set(0.1)
	
	url = item_data['values'][4]
	download_status.set(0.2)
	
	name = item_data['values'][0]
	download_status.set(0.3)
	
	category = item_data['values'][5]
	if login_qbit_status == "True":
		try:
			download_status.set(0.3)
			
			driver = webdriver.Chrome()
			driver.get(url)
			download_status.set(0.5)
			
			magnet_link_element = WebDriverWait(driver, 10).until(
				EC.presence_of_element_located((By.CSS_SELECTOR, "a[href^='magnet:']"))
			)
			magnet_link = magnet_link_element.get_attribute('href')
			download_status.set(0.6)
			
			client = qbittorrentapi.Client(host=qbit_host, username=qbit_username, password=qbit_password)
			download_status.set(0.7)
			
			client.auth_log_in()
			download_status.set(0.8)
			
			client.torrents_add(magnet_link)
			download_status.set(1)
			
			if category == "Movies" or category == "TV":
				download_subtitles_question = CTkMessagebox(icon="question",
				                                            cancel_button_color="transparent",
				                                            title="Download Subtitles?",
				                                            message="It appears you're downloading a movie or tv show, do you want to download subtitles for it?",
				                                            option_1="Yes",
				                                            option_2="No")
				response = download_subtitles_question.get()
				if response == "Yes":
					if login_ost_status == "True":
						create_subtitles_window()
						on_search_button_click(name)
						download_status.set(1)
					else:
						CTkMessagebox(icon="cancel",
				                      cancel_button_color="transparent",
						              title="Error",
						              message=f"You are not logged in to Open Subtitles")
			else:
				return
		except Exception as e:
			CTkMessagebox(icon="cancel",
			              cancel_button_color="transparent",
			              title="Error",
			              message=f"Error: {e}")
		
		finally:
			driver.quit()
	else:
		CTkMessagebox(icon="cancel",
		              cancel_button_color="transparent",
		              title="qBitorrent Login Required",
		              message="Please login to qBitorrent first before attempting the download")
		return


# Opens the Torrent URL in the WebBrowser
def open_torrent_in_browser():
	global site_url, driver
	selected_item = tree.selection()[0]
	item_data = tree.item(selected_item)
	url = item_data['values'][4]
	
	if driver is None:
		driver = webdriver.Chrome()
	
	try:
		driver.get(url)
	except NoSuchWindowException:
		driver = webdriver.Chrome()
		driver.get(url)


# Changes the Size fields to help the Sorting Function
def size_string_to_bytes(size_string):
	size_units = {"B": 1, "KB": 10 ** 3, "MB": 10 ** 6, "GB": 10 ** 9, "TB": 10 ** 12}
	size, unit = size_string.split()
	return float(size) * size_units[unit]


# Converts the Seeds values from example: 1.2k to 1200
def convert_seeds_value(seeds_str):
	if "K" in seeds_str:
		seeds_float = float(seeds_str.replace("K", ""))
		seeds_int = int(seeds_float * 1000)
		return seeds_int
	elif "m" in seeds_str:
		seeds_float = float(seeds_str.replace("m", ""))
		seeds_int = int(seeds_float * 1000000)
		return seeds_int
	else:
		return int(seeds_str)


# Sort the Treeview ascending/descending according to the column selected
def sort_by_column(tree, col, reverse):
	items = [(tree.set(k, col), k) for k in tree.get_children('')]
	
	if col == "Seeds":
		items.sort(key=lambda t: int(t[0]), reverse=reverse)
	elif col == "Size":
		items.sort(key=lambda t: size_string_to_bytes(t[0]), reverse=reverse)
	else:
		items.sort(key=lambda t: t[0].lower(), reverse=reverse)
	
	for index, (_, k) in enumerate(items):
		tree.move(k, '', index)
	
	tree.heading(col, command=lambda: sort_by_column(tree, col, not reverse))


# -----------------------------------------Subtitles Helper Functions-----------------------------------------
def dummy_funtion():
	pass


# Search Subtitles button behaviour
def on_search_button_click(query):
	global ost, subtitles, ost_password, ost_username, login_ost_status, subtitles_language
	ost.logout()
	login_ost_status = "False"
	login = ost.login(ost_username, ost_password)
	login_ost_status = "True"
	if not login:
		CTkMessagebox(icon="cancel",
		              cancel_button_color="transparent",
		              title="Error",
		              message="Login failed. Please check your username and password.")
		return
	
	subtitles_listbox.delete(0, END)
	results = ost.search_subtitles([{'query': query, 'sublanguageid': subtitles_language}])
	
	# Clear the subtitles list and update it with the fetched results
	subtitles.clear()
	subtitles.extend(results)
	
	for i, result in enumerate(results, start=1):
		subtitles_listbox.insert(tk.END, result['SubFileName'])
	return results


# Download Subtitles button behaviour
def on_download_button_click():
	global ost, subtitles
	selected_subtitle_index = subtitles_listbox.curselection()
	if not selected_subtitle_index:
		CTkMessagebox(icon="cancel",
		              cancel_button_color="transparent",
		              title="Error",
		              message="Please select a subtitle to download.")
		return
	selected_subtitle = subtitles[selected_subtitle_index[0]]
	selected_subtitle_id = int(selected_subtitle["IDSubtitleFile"])
	
	subtitle_file_name = os.path.splitext(selected_subtitle["SubFileName"])[0] + ".srt"
	
	url = f"http://dl.opensubtitles.org/en/download/file/{selected_subtitle_id}"
	response = requests.get(url)
	
	if response.status_code == 200:
		save_file_path = filedialog.asksaveasfilename(defaultextension=".srt", initialfile=subtitle_file_name,
		                                              title="Save subtitle as",
		                                              filetypes=[("SRT files", "*.srt"), ("All Files", "*")])
		if save_file_path:
			with open(save_file_path, "wb") as f:
				f.write(response.content)
		else:
			CTkMessagebox(icon="cancel",
			              cancel_button_color="transparent",
			              title="Error!",
			              message="Subtitle download canceled.")
			return
	else:
		CTkMessagebox(icon="cancel",
		              cancel_button_color="transparent",
		              title="Error",
		              message="No subtitles found!.")
	
	ost.logout()


# Sets a global variable to the Subtitle ID selected from the ListBox
def on_select(event):
	global selected_subtitle_index
	selected_subtitle_index = event.widget.curselection()


# -----------------------------------------Menus Creation and Updates-----------------------------------------
def dummy_funtion():
	pass


# Saves the Search History to a JSON file
def save_search_history(query, menu):
	history = load_search_history()
	
	# If the query is already in the history, remove it
	if query in history:
		history.remove(query)
	
	# Add the new or existing query at the beginning
	history.insert(0, query)
	
	# Keep only the last 5 searches
	if len(history) > 5:
		del history[-1]  # Delete the oldest search
	
	with open(search_history_file, "w") as f:
		json.dump(history, f)
	
	update_search_history_menu(menu)


# Loads the Search History from a JSON file
def load_search_history():
	try:
		with open(search_history_file, "r") as f:
			return json.load(f)
	except FileNotFoundError:
		return []


# Updates the Search History SubMenu
def update_search_history_menu(menu):
	menu.delete(0, 'end')
	history = load_search_history()
	
	for item in history:
		if site_url == "https://1337x.unblockit.asia/":
			menu.add_command(label=item, command=lambda query="search/" + item: history_search(query))
		else:
			menu.add_command(label=item, command=lambda query=item: history_search(query))


# Updates the menus
def update_menus():
	global site_url, root, search_history_menu
	empty_menu = Menu(root)
	root.config(menu=empty_menu)
	
	menubar = Menu(root)
	
	filemenu = Menu(menubar, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
	settings_menu = Menu(filemenu, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
	website_menu = Menu(settings_menu, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
	desired_1337x_results_menu = Menu(settings_menu, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
	desired_tgx_results_menu = Menu(settings_menu, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
	desired_solidtorrents_results_menu = Menu(settings_menu, tearoff=0, background="#2b2b2b", fg="white",
	                                          font=("Calibri", 12))
	subtitles_language_menu = Menu(settings_menu, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
	
	searchmenu = Menu(menubar, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
	searchbycatmenu = Menu(searchmenu, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
	searchbycategories = Menu(searchmenu, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
	search_history_menu = Menu(menubar, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
	
	# File Menu
	menubar.add_cascade(label="File", menu=filemenu)
	filemenu.add_command(label="qBitorrent Login", command=lambda: create_qbit_login_window())
	filemenu.add_command(label="Open Subtitles Login", command=lambda: create_ost_login_window())
	filemenu.add_separator()
	
	filemenu.add_cascade(label="Settings", menu=settings_menu)
	
	settings_menu.add_cascade(label="Website to search", menu=website_menu)
	settings_menu.add_separator()
	settings_menu.add_cascade(label="Desired 1337x results", menu=desired_1337x_results_menu)
	settings_menu.add_cascade(label="Desired Torrent Galaxy results", menu=desired_tgx_results_menu)
	settings_menu.add_cascade(label="Desired Solid Torrents Results", menu=desired_solidtorrents_results_menu)
	settings_menu.add_separator()
	settings_menu.add_cascade(label="Subtitles Language", menu=subtitles_language_menu)
	
	filemenu.add_separator()
	
	filemenu.add_command(label="About...", command=lambda: create_about_window())
	
	filemenu.add_separator()
	
	filemenu.add_command(label="Exit", command=lambda: root.destroy())
	
	website_menu.add_command(label="1337x",
	                         command=lambda: save_settings("WebSite", "https://1337x.unblockit.asia/"))
	website_menu.add_command(label="TorrentGalaxy", command=lambda: save_settings("WebSite",
	                                                                              "https://torrentgalaxy.mx/"))
	website_menu.add_command(label="Solid Torrents", command=lambda: save_settings("WebSite",
	                                                                               "https://solidtorrents.to/"))
	
	desired_1337x_results_menu.add_command(label="20", command=lambda: save_settings("Desired_1337x_Results", 2))
	desired_1337x_results_menu.add_command(label="40", command=lambda: save_settings("Desired_1337x_Results", 3))
	desired_1337x_results_menu.add_command(label="60", command=lambda: save_settings("Desired_1337x_Results", 4))
	desired_1337x_results_menu.add_command(label="80", command=lambda: save_settings("Desired_1337x_Results", 5))
	desired_1337x_results_menu.add_command(label="100", command=lambda: save_settings("Desired_1337x_Results", 6))
	desired_1337x_results_menu.add_command(label="120", command=lambda: save_settings("Desired_1337x_Results", 7))
	desired_1337x_results_menu.add_command(label="140", command=lambda: save_settings("Desired_1337x_Results", 8))
	desired_1337x_results_menu.add_command(label="160", command=lambda: save_settings("Desired_1337x_Results", 9))
	desired_1337x_results_menu.add_command(label="180", command=lambda: save_settings("Desired_1337x_Results", 10))
	desired_1337x_results_menu.add_command(label="200", command=lambda: save_settings("Desired_1337x_Results", 11))
	
	desired_tgx_results_menu.add_command(label="50", command=lambda: save_settings("Desired_TorrentGalaxy_Results", 1))
	desired_tgx_results_menu.add_command(label="100", command=lambda: save_settings("Desired_TorrentGalaxy_Results", 2))
	desired_tgx_results_menu.add_command(label="150", command=lambda: save_settings("Desired_TorrentGalaxy_Results", 3))
	desired_tgx_results_menu.add_command(label="200", command=lambda: save_settings("Desired_TorrentGalaxy_Results", 4))
	
	desired_solidtorrents_results_menu.add_command(label="20",
	                                               command=lambda: save_settings("Desired_SOLIDTORRENTS_Results", 2))
	desired_solidtorrents_results_menu.add_command(label="40",
	                                               command=lambda: save_settings("Desired_SOLIDTORRENTS_Results", 3))
	desired_solidtorrents_results_menu.add_command(label="60",
	                                               command=lambda: save_settings("Desired_SOLIDTORRENTS_Results", 4))
	desired_solidtorrents_results_menu.add_command(label="80",
	                                               command=lambda: save_settings("Desired_SOLIDTORRENTS_Results", 5))
	desired_solidtorrents_results_menu.add_command(label="100",
	                                               command=lambda: save_settings("Desired_SOLIDTORRENTS_Results", 6))
	
	subtitles_language_menu.add_command(label="Portuguese", command=lambda: save_settings("Subtitles_Language", "por"))
	subtitles_language_menu.add_command(label="Portuguese - Brazil",
	                                    command=lambda: save_settings("Subtitles_Language", "pob"))
	subtitles_language_menu.add_command(label="English", command=lambda: save_settings("Subtitles_Language", "eng"))
	subtitles_language_menu.add_command(label="French", command=lambda: save_settings("Subtitles_Language", "fra"))
	subtitles_language_menu.add_command(label="Spanish", command=lambda: save_settings("Subtitles_Language", "spa"))
	subtitles_language_menu.add_command(label="Italian", command=lambda: save_settings("Subtitles_Language", "ita"))
	
	# Search Category Menu
	menubar.add_cascade(label="Search by Category", menu=searchmenu)
	
	if site_url == "https://1337x.unblockit.asia/":
		searchbymovies = Menu(searchbycatmenu, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
		searchbytv = Menu(searchbycatmenu, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
		searchbygames = Menu(searchbycatmenu, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
		searchbyapps = Menu(searchbycatmenu, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
		searchbymusic = Menu(searchbycatmenu, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
		searchbydocumentaries = Menu(searchbycatmenu, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
		searchbyanime = Menu(searchbycatmenu, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
		searchbyother = Menu(searchbycatmenu, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
		searchbyxxx = Menu(searchbycatmenu, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
		
		searchmenu.add_command(label="Trending Today",
		                       command=lambda: search_1337x("category", "trending", "trending today"))
		searchmenu.add_command(label="Trending This Week",
		                       command=lambda: search_1337x("category", "trending-week", "trending this week"))
		searchmenu.add_separator()
		
		# Search by Category SubMenu
		searchmenu.add_cascade(label="Search by Trending Categories", menu=searchbycatmenu)
		
		# Categories SubMenus and their respective submenus
		searchbycatmenu.add_cascade(label="Movies", menu=searchbymovies)
		searchbymovies.add_command(label="Today",
		                           command=lambda: search_1337x("category", "trending/d/movies/",
		                                                        "trending Movies today"))
		searchbymovies.add_command(label="This Week",
		                           command=lambda: search_1337x("category", "trending/w/movies/",
		                                                        "trending Movies this week"))
		
		searchbycatmenu.add_cascade(label="TV", menu=searchbytv)
		searchbytv.add_command(label="Today",
		                       command=lambda: search_1337x("category", "trending/d/tv/", "trending Movies today"))
		searchbytv.add_command(label="This Week",
		                       command=lambda: search_1337x("category", "trending/w/tv/", "trending Movies this week"))
		
		searchbycatmenu.add_cascade(label="Games", menu=searchbygames)
		searchbygames.add_command(label="Today",
		                          command=lambda: search_1337x("trending/d/games/", "trending Games today"))
		searchbygames.add_command(label="This Week",
		                          command=lambda: search_1337x("category", "trending/w/games/",
		                                                       "trending Games this week"))
		
		searchbycatmenu.add_cascade(label="Apps", menu=searchbyapps)
		searchbyapps.add_command(label="Today",
		                         command=lambda: search_1337x("category", "trending/d/apps/", "trending Apps today"))
		searchbyapps.add_command(label="This Week",
		                         command=lambda: search_1337x("category", "trending/w/apps/",
		                                                      "trending Apps this week"))
		
		searchbycatmenu.add_cascade(label="Music", menu=searchbymusic)
		searchbymusic.add_command(label="Today",
		                          command=lambda: search_1337x("category", "trending/d/music/", "trending Music today"))
		searchbymusic.add_command(label="This Week",
		                          command=lambda: search_1337x("category", "trending/w/music/",
		                                                       "trending Music this week"))
		
		searchbycatmenu.add_cascade(label="Documentaries", menu=searchbydocumentaries)
		searchbydocumentaries.add_command(label="Today",
		                                  command=lambda: search_1337x("category", "trending/d/documentaries/",
		                                                               "trending Documentaries today"))
		searchbydocumentaries.add_command(label="This Week",
		                                  command=lambda: search_1337x("category", "trending/w/documentaries/",
		                                                               "trending Documentaries this week"))
		
		searchbycatmenu.add_cascade(label="Anime", menu=searchbyanime)
		searchbyanime.add_command(label="Today",
		                          command=lambda: search_1337x("category", "trending/d/anime/", "trending Anime today"))
		searchbyanime.add_command(label="This Week",
		                          command=lambda: search_1337x("category", "trending/w/anime/",
		                                                       "trending Anime this week"))
		
		searchbycatmenu.add_cascade(label="Other", menu=searchbyother)
		searchbyother.add_command(label="Today",
		                          command=lambda: search_1337x("category", "trending/d/other/", "trending Other today"))
		searchbyother.add_command(label="This Week",
		                          command=lambda: search_1337x("category", "trending/w/other/",
		                                                       "trending Other this week"))
		
		searchbycatmenu.add_cascade(label="XXX", menu=searchbyxxx)
		searchbyxxx.add_command(label="Today",
		                        command=lambda: search_1337x("category", "trending/d/xxx/", "trending XXX today"))
		searchbyxxx.add_command(label="This Week",
		                        command=lambda: search_1337x("category", "trending/w/xxx/", "trending XXX this week"))
		
		searchmenu.add_separator()
		
		searchmenu.add_cascade(label="Category", menu=searchbycategories)
		
		searchbycategories.add_command(label="Anime", command=lambda: search_1337x("keyword", "cat/Anime/", "Anime"))
		searchbycategories.add_command(label="Apps", command=lambda: search_1337x("keyword", "cat/Apps/", "Apps"))
		searchbycategories.add_command(label="Documentaries",
		                               command=lambda: search_1337x("keyword", "cat/Documentaries/", "Documentaries"))
		searchbycategories.add_command(label="Games", command=lambda: search_1337x("keyword2", "cat/Games/", "Games"))
		searchbycategories.add_command(label="Movies",
		                               command=lambda: search_1337x("keyword2", "cat/Movies/", "Movies"))
		searchbycategories.add_command(label="Music", command=lambda: search_1337x("keyword2", "cat/Music/", "Music"))
		searchbycategories.add_command(label="Other", command=lambda: search_1337x("keyword2", "cat/Other/", "Other"))
		searchbycategories.add_command(label="TV", command=lambda: search_1337x("keyword2", "cat/TV/", "TV"))
		searchbycategories.add_command(label="XXX", command=lambda: search_1337x("keyword2", "cat/XXX/", "XXX"))
	
	elif site_url == "https://torrentgalaxy.mx/":
		
		searchbycategories_anime = Menu(searchmenu, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
		searchbycategories_apps = Menu(searchmenu, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
		searchbycategories_books = Menu(searchmenu, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
		searchbycategories_docus = Menu(searchmenu, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
		searchbycategories_games = Menu(searchmenu, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
		searchbycategories_movies = Menu(searchmenu, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
		searchbycategories_music = Menu(searchmenu, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
		searchbycategories_other = Menu(searchmenu, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
		searchbycategories_tv = Menu(searchmenu, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
		searchbycategories_xxx = Menu(searchmenu, tearoff=0, background="#2b2b2b", fg="white", font=("Calibri", 12))
		
		searchmenu.add_cascade(label="Anime", menu=searchbycategories_anime)
		searchbycategories_anime.add_command(label="All",
		                                     command=lambda: search_torrent_galaxy("category", "cat=28", "Anime - All"))
		searchmenu.add_separator()
		
		searchmenu.add_cascade(label="Apps", menu=searchbycategories_apps)
		searchbycategories_apps.add_command(label="Mobile",
		                                    command=lambda: search_torrent_galaxy("category", "cat=20",
		                                                                          "Apps - Mobile"))
		searchbycategories_apps.add_command(label="Other",
		                                    command=lambda: search_torrent_galaxy("category", "cat=21", "Apps - Other"))
		searchbycategories_apps.add_command(label="Windows",
		                                    command=lambda: search_torrent_galaxy("category", "cat=18",
		                                                                          "Apps - Windows"))
		searchmenu.add_separator()
		
		searchmenu.add_cascade(label="Books", menu=searchbycategories_books)
		searchbycategories_books.add_command(label="Audiobooks",
		                                     command=lambda: search_torrent_galaxy("category", "cat=13",
		                                                                           "Books - Audiobooks"))
		searchbycategories_books.add_command(label="Comics",
		                                     command=lambda: search_torrent_galaxy("category", "cat=19",
		                                                                           "Books - Comics"))
		searchbycategories_books.add_command(label="Ebooks",
		                                     command=lambda: search_torrent_galaxy("category", "cat=12",
		                                                                           "Books - Ebooks"))
		searchbycategories_books.add_command(label="Educational",
		                                     command=lambda: search_torrent_galaxy("category", "cat=14",
		                                                                           "Books - Educational"))
		searchbycategories_books.add_command(label="Magazine",
		                                     command=lambda: search_torrent_galaxy("category", "cat=15",
		                                                                           "Books - Magazine"))
		searchmenu.add_separator()
		
		searchmenu.add_cascade(label="Documentaries", menu=searchbycategories_docus)
		searchbycategories_docus.add_command(label="All",
		                                     command=lambda: search_torrent_galaxy("category", "cat=9", "Docus - All"))
		searchmenu.add_separator()
		
		searchmenu.add_cascade(label="Games", menu=searchbycategories_games)
		searchbycategories_games.add_command(label="Others",
		                                     command=lambda: search_torrent_galaxy("category", "cat=43",
		                                                                           "Games - Others"))
		searchbycategories_games.add_command(label="Windows",
		                                     command=lambda: search_torrent_galaxy("category", "cat=10",
		                                                                           "Games - Windows"))
		searchmenu.add_separator()
		
		searchmenu.add_cascade(label="Movies", menu=searchbycategories_movies)
		searchbycategories_movies.add_command(label="CAM/TS",
		                                      command=lambda: search_torrent_galaxy("category", "cat=45",
		                                                                            "Movies - CAM/TS"))
		searchbycategories_movies.add_command(label="SD",
		                                      command=lambda: search_torrent_galaxy("category", "cat=1", "Movies - SD"))
		searchbycategories_movies.add_command(label="HD",
		                                      command=lambda: search_torrent_galaxy("category", "cat=42",
		                                                                            "Movies - HD"))
		searchbycategories_movies.add_command(label="4K UHD",
		                                      command=lambda: search_torrent_galaxy("category", "cat=3",
		                                                                            "Movies - 4K UHD"))
		searchbycategories_movies.add_command(label="Packs",
		                                      command=lambda: search_torrent_galaxy("category", "cat=4",
		                                                                            "Movies - Packs"))
		searchbycategories_movies.add_command(label="Bollywood",
		                                      command=lambda: search_torrent_galaxy("category", "cat=46",
		                                                                            "Movies - Bollywood"))
		searchmenu.add_separator()
		
		searchmenu.add_cascade(label="Music", menu=searchbycategories_music)
		searchbycategories_music.add_command(label="Lossless",
		                                     command=lambda: search_torrent_galaxy("category", "cat=23",
		                                                                           "Music - Lossless"))
		searchbycategories_music.add_command(label="Singles",
		                                     command=lambda: search_torrent_galaxy("category", "cat=24",
		                                                                           "Music - Singles"))
		searchbycategories_music.add_command(label="Albums",
		                                     command=lambda: search_torrent_galaxy("category", "cat=22",
		                                                                           "Music - Albums"))
		searchbycategories_music.add_command(label="Discography",
		                                     command=lambda: search_torrent_galaxy("category", "cat=26",
		                                                                           "Music - Discography"))
		searchbycategories_music.add_command(label="MusicVideo",
		                                     command=lambda: search_torrent_galaxy("category", "cat=25",
		                                                                           "Music - MusicVideo"))
		searchmenu.add_separator()
		
		searchmenu.add_cascade(label="Other", menu=searchbycategories_other)
		searchbycategories_other.add_command(label="Audio",
		                                     command=lambda: search_torrent_galaxy("category", "cat=17",
		                                                                           "Other - Audio"))
		searchbycategories_other.add_command(label="Other",
		                                     command=lambda: search_torrent_galaxy("category", "cat=40",
		                                                                           "Other - Other"))
		searchbycategories_other.add_command(label="Pictures",
		                                     command=lambda: search_torrent_galaxy("category", "cat=37",
		                                                                           "Other - Pictures"))
		searchbycategories_other.add_command(label="Training",
		                                     command=lambda: search_torrent_galaxy("category", "cat=33",
		                                                                           "Other - Training"))
		searchmenu.add_separator()
		
		searchmenu.add_cascade(label="TV", menu=searchbycategories_tv)
		searchbycategories_tv.add_command(label="Episodes SD",
		                                  command=lambda: search_torrent_galaxy("category", "cat=5",
		                                                                        "TV - Episodes SD"))
		searchbycategories_tv.add_command(label="Episodes HD",
		                                  command=lambda: search_torrent_galaxy("category", "cat=41",
		                                                                        "TV - Episodes HD"))
		searchbycategories_tv.add_command(label="Episodes 4K UHD",
		                                  command=lambda: search_torrent_galaxy("category", "cat=11",
		                                                                        "TV - Episodes 4K UHD"))
		searchbycategories_tv.add_command(label="Packs",
		                                  command=lambda: search_torrent_galaxy("category", "cat=6", "TV - Packs"))
		searchmenu.add_separator()
		
		searchmenu.add_cascade(label="XXX", menu=searchbycategories_xxx)
		searchbycategories_xxx.add_command(label="SD",
		                                   command=lambda: search_torrent_galaxy("category", "cat=34", "XXX - SD"))
		searchbycategories_xxx.add_command(label="HD",
		                                   command=lambda: search_torrent_galaxy("category", "cat=35", "XXX - HD"))
		searchbycategories_xxx.add_command(label="Misc",
		                                   command=lambda: search_torrent_galaxy("category", "cat=47", "XXX - Misc"))
	
	elif site_url == "https://solidtorrents.to/":
		searchmenu.add_command(label="Trending Top 100 Torrents",
		                       command=lambda: search_solidtorrents("top100", "trending", "Trending Top 100 Torrents"))
		searchmenu.add_separator()
		
		searchmenu.add_command(label="Games",
		                       command=lambda: search_solidtorrents("category", "search?q=&category=6&subcat=1",
		                                                            "Games"))
		searchmenu.add_command(label="Music", command=lambda: search_solidtorrents("category", "music", "Music"))
		searchmenu.add_command(label="Software",
		                       command=lambda: search_solidtorrents("category", "softwares", "Software"))
		searchmenu.add_command(label="Videos", command=lambda: search_solidtorrents("category", "videos", "Videos"))
	
	# Search History Menu
	menubar.add_cascade(label="Search History", menu=search_history_menu)
	
	# Update Search History Menu
	update_search_history_menu(search_history_menu)
	# Menus Separator between Torrens and Subtitles
	menubar.add_separator()
	menubar.add_separator()
	menubar.add_separator()
	menubar.add_separator()
	menubar.add_separator()
	# Subtitles Search Menu
	menubar.add_command(label="Search for Subtitles", command=lambda: create_subtitles_window())
	
	# Start Menus
	root.config(menu=menubar)


# -----------------------------------------Loading and Saving values-----------------------------------------
def dummy_funtion():
	pass


# Logs into qBitorrent and Saves the Login Credentials to a JSON file
def save_qbit_credentials(login_qbit_window):
	global qbit_username, qbit_password, qbit_host, login_qbit_status, entry_qbit_username, entry_qbit_password, entry_qbit_host, var_qbit_store_credentials
	
	new_credentials = {
		"qbit_username": entry_qbit_username.get(),
		"qbit_password": entry_qbit_password.get(),
		"qbit_host": entry_qbit_host.get()
	}
	
	if var_qbit_store_credentials.get():
		if os.path.exists(credentials_file):
			with open(credentials_file, "r") as f:
				existing_credentials = json.load(f)
		else:
			existing_credentials = {}
		
		existing_credentials.update(new_credentials)
		
		with open(credentials_file, "w") as f:
			json.dump(existing_credentials, f)
	
	qbit_username = entry_qbit_username.get()
	qbit_password = entry_qbit_password.get()
	qbit_host = entry_qbit_host.get()
	login_qbit_status = "True"
	
	login_qbit_window.destroy()


# Logs into Open Subtitles and Saves the Login Credentials to a JSON file
def save_ost_credentials(login_ost_window, entry_ost_username, entry_ost_password, var_ost_store_credentials):
	global ost_username, ost_password, login_ost_status
	
	new_credentials = {
		"ost_username": entry_ost_username,
		"ost_password": entry_ost_password
	}
	
	if var_ost_store_credentials:
		if os.path.exists(credentials_file):
			with open(credentials_file, "r") as f:
				existing_credentials = json.load(f)
		else:
			existing_credentials = {}
		
		existing_credentials.update(new_credentials)
		
		with open(credentials_file, "w") as f:
			json.dump(existing_credentials, f)
	
	ost_username = entry_ost_username
	ost_password = entry_ost_password
	login_ost_status = "True"
	
	login_ost_window.destroy()


# Loads the Login Credentials from a JSON file
def load_credentials():
	global ost_username, ost_password, qbit_username, qbit_password, qbit_host
	if os.path.exists(credentials_file):
		with open(credentials_file, "r") as f:
			credentials = json.load(f)
			
			qbit_username = credentials["qbit_username"]
			qbit_password = credentials["qbit_password"]
			qbit_host = credentials["qbit_host"]
			
			ost_username = credentials["ost_username"]
			ost_password = credentials["ost_password"]


# Sets default values for Settings in case there aren't any
def set_default_values(settings):
	default_desired_results = 2
	default_tgx_desired_results = 1
	default_solidtorrents_desired_results = 2
	default_website = "https://torrentgalaxy.mx/"
	default_subtitles_language = "por"
	
	if "Desired_1337x_Results" not in settings:
		settings["Desired_1337x_Results"] = default_desired_results
	if "Desired_SOLIDTORRENTS_Results" not in settings:
		settings["Desired_SOLIDTORRENTS_Results"] = default_solidtorrents_desired_results
	if "Desired_TorrentGalaxy_Results" not in settings:
		settings["Desired_TorrentGalaxy_Results"] = default_tgx_desired_results
	if "WebSite" not in settings:
		settings["WebSite"] = default_website
	if "Subtitles_Language" not in settings:
		settings["Subtitles_Language"] = default_subtitles_language
	
	return settings


# Saves the Settings Values to a JSON File
def save_settings(query, amount):
	global desired_results, site_url, desired_tgx_results, desired_solidtorrents_results
	
	settings = load_settings()
	settings[query] = amount
	
	with open(settings_file, "w") as f:
		json.dump(settings, f)
	
	settings = set_default_values(settings)
	
	desired_results = settings["Desired_1337x_Results"]
	desired_solidtorrents_results = settings["Desired_SOLIDTORRENTS_Results"]
	desired_tgx_results = settings["Desired_TorrentGalaxy_Results"]
	site_url = settings["WebSite"]
	
	update_menus()


# Loads the Settings Values from a JSON File
def load_settings():
	global desired_results, site_url, desired_tgx_results, desired_solidtorrents_results, subtitles_language
	
	default_desired_results = 2
	default_tgx_desired_results = 1
	default_solidtorrents_desired_results = 2
	default_website = "https://1337x.unblockit.asia/"
	default_subtitles_language = "por"
	
	try:
		with open(settings_file, "r") as f:
			settings = json.load(f)
			
			if "Desired_1337x_Results" not in settings:
				settings["Desired_1337x_Results"] = default_desired_results
			else:
				desired_results = settings["Desired_1337x_Results"]
			
			if "Desired_SOLIDTORRENTS_Results" not in settings:
				settings["Desired_SOLIDTORRENTS_Results"] = default_solidtorrents_desired_results
			else:
				desired_solidtorrents_results = settings["Desired_SOLIDTORRENTS_Results"]
			
			if "Desired_TorrentGalaxy_Results" not in settings:
				settings["Desired_TorrentGalaxy_Results"] = default_tgx_desired_results
			else:
				desired_tgx_results = settings["Desired_TorrentGalaxy_Results"]
			
			if "WebSite" not in settings:
				settings["WebSite"] = default_website
				site_url = settings["WebSite"]
			else:
				site_url = settings["WebSite"]
			
			if "Subtitles_Language" not in settings:
				settings["Subtitles_Language"] = default_subtitles_language
			else:
				subtitles_language = settings["Subtitles_Language"]
	
	except (FileNotFoundError, json.JSONDecodeError):
		settings = set_default_values(settings)
		save_settings()
	
	return settings


# -----------------------------------------Windows Creation-----------------------------------------
def dummy_funtion():
	pass


# Creates the Subtitles Search Window
def create_subtitles_window():
	global subtitles_window, subtitles_listbox
	
	# Subtitles entry focus in event
	def on_focus_in(event):
		if movie_entry.get() == 'Enter movie name...':
			movie_entry.delete(0, tk.END)
	
	# Subtitles Window
	subtitles_window = ctk.CTk()
	subtitles_window.title("Subtitles Download")
	subtitles_window.config(bg="#2b2b2b")
	subtitles_window.geometry(f"{480}x{350}")
	subtitles_window.resizable(False, False)
	subtitles_window.eval("tk::PlaceWindow . Center")
	
	# Subtitles Frames
	subtitles_frame1 = ctk.CTkFrame(subtitles_window)
	subtitles_frame1.pack(fill="x", expand=True)
	subtitles_frame2 = ctk.CTkFrame(subtitles_window)
	subtitles_frame2.pack(fill="x", expand=True)
	subtitles_frame3 = ctk.CTkFrame(subtitles_window)
	subtitles_frame3.pack(fill="x", expand=True)
	
	# Subtitles Widgets
	label = ctk.CTkLabel(master=subtitles_frame1, text="Movie Name:", height=28)
	label.grid(row=0, column=0, sticky='w', pady=10, padx=20)
	
	movie_entry = ctk.CTkEntry(master=subtitles_frame1, width=150, height=28)
	movie_entry.insert(0, 'Enter movie name...')
	movie_entry.bind('<FocusIn>', on_focus_in)
	movie_entry.grid(row=0, column=1, pady=10, padx=20)
	
	search_subtitles_button = ctk.CTkButton(master=subtitles_frame1, text="Search",
	                                        command=lambda: on_search_button_click(movie_entry.get()), height=56)
	search_subtitles_button.grid(row=0, column=2, pady=10, padx=20, rowspan=2)
	
	subtitles_listbox = tk.Listbox(master=subtitles_frame2, selectmode=tk.SINGLE, font=('Calibri', 15), bg="#2b2b2b",
	                               fg='white',
	                               height=10,
	                               width=55
	                               )
	subtitles_listbox.pack(fill="x", expand=True, pady=(20, 0))
	subtitles_listbox.bind('<<ListboxSelect>>', on_select)
	
	download_button = ctk.CTkButton(master=subtitles_frame3, text="Download Subtitle",
	                                command=lambda: on_download_button_click(),
	                                height=28)
	download_button.pack(pady=10, padx=20)


# Creates the About Window
def create_about_window():
	# About Window
	about_window = ctk.CTk()
	about_window.title("About...")
	about_window.config(bg="#2b2b2b")
	about_window.geometry(f"{300}x{100}")
	about_window.resizable(False, False)
	about_window.eval("tk::PlaceWindow . Center")
	
	# About Frames
	about_frame1 = ctk.CTkFrame(about_window)
	about_frame1.pack(fill="x", expand=True)
	
	# About Widgets
	about_label_1 = ctk.CTkLabel(about_frame1, text="Torrent Finder and Subtitles Downloader AIO")
	about_label_1.pack()
	
	about_separator = ctk.CTkLabel(about_frame1, text="", height=10)
	about_separator.pack()
	
	about_label_2 = ctk.CTkLabel(about_frame1, text="        Version: 0.1.2")
	about_label_2.pack(side="left")


# Creates the Open Subtitles Login Window
def create_ost_login_window():
	global ost_username, ost_password
	
	# OST Login Window
	login_ost_window = ctk.CTk()
	login_ost_window.title("Open Subtitles Login")
	login_ost_window.config(bg="#2b2b2b")
	login_ost_window.resizable(False, False)
	login_ost_window.focus()
	login_ost_window.protocol("WM_DELETE_WINDOW", toggle_window(login_ost_window))
	
	# Center OST Login Window
	w = 270
	h = 180
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
	x = (screen_width / 2)
	y = (screen_height / 2) - (h / 2)
	login_ost_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
	
	# OST Login Frame
	ost_login_frame = ctk.CTkFrame(login_ost_window)
	ost_login_frame.pack(padx=10, pady=10)
	
	# OST Login Widgets
	ctk.CTkLabel(ost_login_frame, text="Username:").grid(row=0, column=0, sticky="e", pady=(0, 5), padx=5)
	entry_ost_username = ctk.CTkEntry(ost_login_frame)
	entry_ost_username.grid(row=0, column=1, pady=5, padx=5)
	
	ctk.CTkLabel(ost_login_frame, text="Password:").grid(row=1, column=0, sticky="e", pady=5, padx=5)
	entry_ost_password = ctk.CTkEntry(ost_login_frame, show="*")
	entry_ost_password.grid(row=1, column=1, pady=5, padx=5)
	
	var_ost_store_credentials = tk.BooleanVar(value=True)
	check_store_credentials = ctk.CTkCheckBox(ost_login_frame, text="Save credentials",
	                                          variable=var_ost_store_credentials)
	check_store_credentials.grid(row=3, columnspan=2, pady=5, padx=5)
	
	submit_button = ctk.CTkButton(ost_login_frame, text="Submit",
	                              command=lambda: save_ost_credentials(login_ost_window, entry_ost_username.get(),
	                                                                   entry_ost_password.get(),
	                                                                   var_ost_store_credentials))
	submit_button.grid(row=4, columnspan=2, pady=(10, 0))
	
	entry_ost_username.insert(0, ost_username)
	entry_ost_password.insert(0, ost_password)


# Creates the qBitorrent Login Window
def create_qbit_login_window():
	global qbit_username, qbit_password, qbit_host, entry_qbit_username, entry_qbit_password, entry_qbit_host, var_qbit_store_credentials
	
	# QBitorrent Login Window
	login_qbit_window = ctk.CTk()
	login_qbit_window.title("qBitorrent Login")
	login_qbit_window.config(bg="#2b2b2b")
	login_qbit_window.resizable(False, False)
	login_qbit_window.focus()
	login_qbit_window.protocol("WM_DELETE_WINDOW", toggle_window(login_qbit_window))
	
	# Center QBitorrent Login Window
	w = 270
	h = 220
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
	x = (screen_width / 2)
	y = (screen_height / 2) - (h / 2)
	login_qbit_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
	
	# QBitorrent Login Frame
	qbit_login_frame = ctk.CTkFrame(login_qbit_window)
	qbit_login_frame.pack(padx=10, pady=10)
	
	# QBitorrent Login Widgets
	ctk.CTkLabel(qbit_login_frame, text="Username:").grid(row=0, column=0, sticky="e", pady=(0, 5), padx=5)
	entry_qbit_username = ctk.CTkEntry(qbit_login_frame)
	entry_qbit_username.grid(row=0, column=1, pady=5, padx=5)
	
	ctk.CTkLabel(qbit_login_frame, text="Password:").grid(row=1, column=0, sticky="e", pady=5, padx=5)
	entry_qbit_password = ctk.CTkEntry(qbit_login_frame, show="*")
	entry_qbit_password.grid(row=1, column=1, pady=5, padx=5)
	
	ctk.CTkLabel(qbit_login_frame, text="Host:").grid(row=2, column=0, sticky="e", pady=5, padx=5)
	entry_qbit_host = ctk.CTkEntry(qbit_login_frame)
	entry_qbit_host.grid(row=2, column=1, pady=5, padx=5)
	
	var_qbit_store_credentials = tk.BooleanVar(value=True)
	check_store_credentials = ctk.CTkCheckBox(qbit_login_frame, text="Save credentials",
	                                          variable=var_qbit_store_credentials)
	check_store_credentials.grid(row=3, columnspan=2, pady=5, padx=5)
	
	submit_button = ctk.CTkButton(qbit_login_frame, text="Submit",
	                              command=lambda: save_qbit_credentials(login_qbit_window))
	submit_button.grid(row=4, columnspan=2, pady=(10, 0))
	
	entry_qbit_username.insert(0, qbit_username)
	entry_qbit_password.insert(0, qbit_password)
	entry_qbit_host.insert(0, qbit_host)


# -----------------------------------------Windows Behaviour-----------------------------------------
def dummy_funtion():
	pass


# Hides the Sub Windows
def toggle_window(window):
	state = window.state()
	if state == "normal":
		window.withdraw()
	elif state == "iconic":
		window.withdraw()
	elif state == "withdrawn":
		window.deiconify()


# -----------------------------------------Main Program Loop-----------------------------------------
if __name__ == "__main__":
	# Main Window
	root = ctk.CTk()
	root.title("Torrent Finder")
	root.config(bg="#2b2b2b")
	root.geometry("700x70")
	root.resizable(False, False)
	root.eval("tk::PlaceWindow . Center")
	root.protocol("WM_DELETE_WINDOW", exit)
	
	# Frames
	frame1 = ctk.CTkFrame(root)
	frame1.pack(padx=10, pady=(10, 10))
	
	frame2 = ctk.CTkFrame(root)
	frame2.pack(padx=10, pady=10)
	
	frame3 = ctk.CTkFrame(root)
	frame3.pack(padx=10, pady=10)
	
	frame4 = ctk.CTkFrame(root)
	frame4.pack(padx=10, pady=10)
	
	# Search Widgets
	keyword_label = ctk.CTkLabel(frame1, text="Search Keyword:")
	keyword_label.grid(row=0, column=0)
	
	keyword_entry = ctk.CTkEntry(frame1)
	keyword_entry.grid(row=0, column=1)
	
	search_button = ctk.CTkButton(frame1, text="Search",
	                              command=lambda: search_button_click("keyword",
	                                                                  keyword_entry.get(),
	                                                                  keyword_entry.get()
	                                                                  )
	                              )
	search_button.grid(row=0, column=2)
	
	# Treeview
	style = ttk.Style()
	style.configure('Treeview', background='#2b2b2b', foreground='white', fieldbackground='#2b2b2b')
	
	tree = ttk.Treeview(frame2,
	                    selectmode="browse",
	                    columns=("Name",
	                             "Seeds",
	                             "Size",
	                             "Uploader",
	                             "URL",
	                             "Category",
	                             "Dummy Column"),
	                    show="headings", height=20
	                    )
	
	# Treeview Columns Creation
	tree.heading("Name", text="Name", command=lambda: sort_by_column(tree, "Name", False))
	tree.column("Name", minwidth=0, width=450, stretch=False)
	
	tree.heading("Seeds", text="Seeds", command=lambda: sort_by_column(tree, "Seeds", False))
	tree.column("Seeds", minwidth=0, width=50, stretch=False, anchor="center")
	
	tree.heading("Size", text="Size", command=lambda: sort_by_column(tree, "Size", False))
	tree.column("Size", minwidth=0, width=60, stretch=False, anchor="e")
	
	tree.heading("Uploader", text="Uploader", anchor="w", command=lambda: sort_by_column(tree, "Uploader", False))
	tree.column("Uploader", minwidth=0, width=100, stretch=False, anchor="w")
	
	tree.heading("URL", text="URL", command=lambda: sort_by_column(tree, "URL", False))
	tree.column("URL", minwidth=0, width=80, stretch=False, anchor="center")
	
	tree.heading("Category", text="Category", command=lambda: sort_by_column(tree, "Category", False))
	tree.column("Category", minwidth=0, width=80, stretch=False, anchor="center")
	
	tree.heading("Dummy Column", text="")
	tree.column("Dummy Column", minwidth=0, width=20, stretch=True, anchor="center")
	
	tree.place(relx=0.4, rely=0.5, anchor="w")
	tree.pack()
	
	# Scrollbar Implementation
	scrollbar = ttk.Scrollbar(frame2, orient=tk.VERTICAL, command=tree.yview)
	tree.configure(yscroll=scrollbar.set)
	scrollbar.place(relx=1, rely=0.53, anchor="e", height=400)
	
	# Download Widgets
	open_in_browser_button = ctk.CTkButton(frame3, text="Open Selected Torrent in WebBrowser",
	                                       command=open_torrent_in_browser)
	open_in_browser_button.pack(side='left')
	
	ctk.CTkLabel(frame3, text="", width=270).pack(side='left', fill='both', expand=False)
	
	download_button = ctk.CTkButton(frame3, text="Download Selected Torrent", command=download_torrent)
	download_button.pack(side='right')
	
	download_status = ctk.CTkProgressBar(frame4, orientation="horizontal", width=500)
	download_status.pack()
	download_status.set(0)
	
	# Load saved credentials and settings at startup
	load_credentials()
	load_settings()
	
	update_menus()
	
	root.mainloop()
