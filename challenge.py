import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import csv
import re

class Wikicrawler():
  """
    Crawls Wikipedia starting from 500 random pages and tracks the click
    path to the Philosophy Wikipedia page.
  """

  def __init__(self):
    self.base_url = "https://en.wikipedia.org"
    self.philosophy = "https://en.wikipedia.org/wiki/Philosophy"
    self.visited_urls = {} #Used to store urls as keys and path length as values
    self.unavailable = {} #Used to store urls that do not reach Philosphy page. Value = -1
    self.counter = 0 #Path length from starting random page
    self.paths_tested = 0 #Counter for total number of pages tried.
    self.path_length_dict = {} #For distribution graphing. Key = path length: Value = Frequency
    self.wikilink = r'(?<=<a href=")/wiki/[a-zA-Z\(\)\-\,_#]*?(?=")' #Regex for href to the next link


  def crawler(self, start_page):
    """
      Args: start_page - the starting page as a string
      Returns:  1 on succes of entering a url entry to one of the two dictionaries
    """

    route_length = self.philosophy_test(start_page)
    if route_length >= 0: #In case of successful path to Philosophy page
      self.visited_urls[start_page] = route_length
      return 1
    elif route_length == -1: #In case of failure to reach Philosophy page
      self.unavailable[start_page] = -1
      return 1
    else:
      print("error line 38") #error message should not be reached


  def next_link(self, url):
    """
      Args: url - url to be parsed as a string
      Returns: the next page to be assessed or a kick out if no next page
    """
    r = requests.get(url)
    page = r.text
    soup = BeautifulSoup(page, 'html.parser') #inputs the text from the page and parses it
    body = soup.select('div#mw-content-text > p') #body becomes all p elements in the content div
    if body == None: #check to make sure there is a body
      return -100
    cleaned_body = self.remove_parenthesis(str(body)) #take out strings between parentheses
    match = re.search(self.wikilink, cleaned_body) #checks the cleaned_body for next wiki page link using regex
    if match:
      href = match.group(0).split('#')[0] #next page link
      if href == '': #if href is not a link
        href = self.check_if_list(soup) #check to see href is in an li element
      new_page = self.base_url + href
      return new_page #next page url
    elif not match: #if no link return the kickout to say no path possible
        return -100

  def check_if_list(self, soup):
    """
      Checks to see if link is in a li element if no links in p elements

      Args: soup - parsed html
      Returns: Link suffix if there is a link, else False
    """
    body_list = soup.select('div#mw-content-text > ul > li')
    cleaned_body = self.remove_parenthesis(str(body_list))
    match = re.search(self.wikilink, cleaned_body)
    if match != 0:
      href = match.group(0).split('#')[0]
      if href != None:
        return href
      else:
        return False
    else:
      return False

  def remove_parenthesis(self, text):
    """
      Removes content between parenthesis from a string,
      but leaves <tags> alone.

      Args: string - the body must be turned into a string
      Returns: The body of the text with content(s) between parentesis removed
    """
    paren_counter = 0 # becomes 0 (closed) or 1 (open) to check if parenthesis is open or closed
    tag_counter = 0 #becomes 0 or 1 to check if tag is open or closed
    cleaned = ''
    for i in text:
      if i == '<':
        tag_counter += 1
      elif i == '>':
        tag_counter -= 1
      elif i == '(' and tag_counter == 0:
        paren_counter += 1
      elif i == ')' and tag_counter == 0:
        paren_counter -= 1
      if paren_counter == 0:
        cleaned += i
    return cleaned

  def philosophy_test(self, url):
    """
      Checks to see relation to Philosophy page

      Args: url - string of url being assessed
      Returns: counter or -1 if no possible relation to philosophy page
    """
    if url == -100: #in case of no path to Philosophy page
      return -1

    if url == self.philosophy: # in case of reaching Philosophy page
      return self.counter

    elif url in self.visited_urls: #in case of reaching a page already stored in visited_urls dictionary
      counter = self.counter + self.visited_urls[url]
      return counter

    elif self.counter >= 45: #limits path searches to 45 clicks to limit possible infinite loops
      return -1

    elif url != self.philosophy: #recursively call function to keep going until path is resolved
      self.counter += 1
      next_url = self.next_link(url)
      test = self.philosophy_test(next_url)
      return test
    else:
      return -100 #should not hit this error

  def write_csv(self):
    """
      Turns the results into a csv file
      Url is in one column, and path length is in another column.
    """
    with open('data.csv', 'w') as csvfile:
      fieldnames = ['url', 'clicks']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

      writer.writeheader()
      for key, value in self.visited_urls.items():
        writer.writerow({'url': key, 'clicks': value})
      for key, value in self.unavailable.items():
        writer.writerow({'url': key, 'clicks': value})

  def percent(self):
    """
      Checks successful rate of linking to Philosophy page
    """
    success = len(self.visited_urls) #checks length of visited_urls dic
    print("success: ", success)
    failed = len(self.unavailable) #checks length of unavailable dic
    print("failed: ", failed)
    total = success + failed
    percentage = success/total #creates percentage
    return percentage

  def distribution(self):
    """
      Sets x and y axis and plots distribution using matplotlib for successful paths
    """
    xaxis = [] #path lengths
    yaxis = [] #frequency

    for key, value in self.visited_urls.items():
      if value not in self.path_length_dict: #adds new paths lengths to dictionary
        self.path_length_dict[value] = 1
      else: #adds frequecnty to dictionary
        self.path_length_dict[value] += 1

    for key in self.path_length_dict.keys(): #adds to the x and y axis lists
      xaxis.append(int(key))
      yaxis.append(int(self.path_length_dict[key]))

    #Plots data and creates a png file named 'plot'
    plt.bar(xaxis, yaxis, align='center')
    plt.xlabel('Path Length')
    plt.ylabel('Frequency')
    plt.title('Random Wikipedia Page Path Length to the Philosophy Page Frequency')
    plt.savefig('plot.png')




  def run(self):
    """
      Run this function to run program.

      Returns Success Rate
    """
    self.counter = 0 #resets counter for each starting page
    random_url = self.base_url + "/wiki/Special:Random"
    start_page = requests.get(random_url)
    start_page_url = start_page.url #gets the landing url
    path_tested = self.crawler(start_page_url) #starts the crawling and returns 1 once finished
    self.paths_tested = self.paths_tested + path_tested #adds 1 to paths_tested for each completion of path
    print(self.paths_tested) #Shows progress in terminal
    if self.paths_tested >= 500: #stops paths tested at 500
      percentage = self.percent() #on completion check Pecent of successful paths
      print("%: ", percentage)
      distribution = self.distribution() #on completion plot distribution
      self.write_csv() #on completion write data to a csv file
      return percentage
    else:
      self.run() #run recursive function until we test 500 random starting points



pager = Wikicrawler()
pager.run()

