from typing import Counter
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
import time
from urllib.parse import unquote


class Wikipage:
    def __init__(self, url: str, driver: WebDriver):
        self.driver = driver
        self.heading: str = None
        self.url: str = url
        self.main_paragraphs: list[WebElement] = []
        self.usable_links: list[WebElement] = []
        self.load()

    def is_in_parenthesis(self, paragraph: str, index: int, left: str, right: str) -> bool:
        unclosed_brackets = 0
        for i in range(0, index):
            if paragraph[i] == left:
                unclosed_brackets += 1
            elif paragraph[i] == right:
                unclosed_brackets -= 1

        return unclosed_brackets != 0

    def load_all_usable_links(self):

        for p in self.main_paragraphs:
            links = p.find_elements_by_tag_name("a")
            for l in links:

                parent: WebElement = l.find_element_by_xpath("..")
                if parent.tag_name == "i":
                    continue
                elif l.text.startswith("[") and l.text.endswith("]"):
                    continue
                elif self.is_in_parenthesis(p.text, p.text.find(l.text), "(", ")"):
                    continue
                elif l.text == "":
                    continue
                # Get rid of selflink without href
                elif l.get_attribute("href") == None:
                    continue
                # Get rid of all outside links
                elif not l.get_attribute("href").startswith("https://en.wikipedia.org"):
                    continue
                else:
                    self.usable_links.append(l)
                    break

    def load(self):
        self.driver.get(self.url)
        self.heading = self.driver.find_element_by_id("firstHeading")
        self.main_paragraphs = self.driver.find_element_by_id(
            "mw-content-text").find_elements_by_xpath("//div[@class='mw-parser-output']/p")
        self.load_all_usable_links()

    def get_nth_usable_link(self, index: int):
        if index in range(len(self.usable_links)):
            link = self.usable_links[index]
            return link
        else:
            return None

    def click_link(self, index):
        url = self.usable_links[0].get_property("href")
        self.usable_links[0].click()
        return Wikipage(url, self.driver)


url = "https://en.wikipedia.org/wiki/Special:Random"
#url = "https://en.wikipedia.org/wiki/Science"

driver = webdriver.Chrome()
page = Wikipage(url, driver)


transitions = 0
visited_links = [page.driver.current_url]

while(page.heading.text != "Philosophy"):

    url = page.get_nth_usable_link(0)
    if url in visited_links:
        print("Whoops, loop! Ending application!")
        break
    else:
        visited_links.append(url.get_attribute("href"))
        page = page.click_link(url)
        time.sleep(1)
        transitions += 1


print("Application made {} transitions and visited folowing links: ".format(transitions))
for visited_link in visited_links:
    print(visited_link)
