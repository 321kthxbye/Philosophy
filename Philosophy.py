from typing import Counter
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
import time


def is_in_parenthesis(paragraph: str, index : int, left : str, right : str) -> bool:
    unclosed_brackets = 0
    for i in range(0, index):
        if paragraph[i] == left:
            unclosed_brackets += 1
        elif paragraph[i] == right:
            unclosed_brackets -= 1

    return unclosed_brackets != 0


driver = webdriver.Chrome()
url = "https://en.wikipedia.org/wiki/Special:Random"
# url = "https://en.wikipedia.org/wiki/egg"
#url = "https://en.wikipedia.org/wiki/Eukaryote"
#url = "https://en.wikipedia.org/wiki/Uncertainty"
# url = "https://en.wikipedia.org/wiki/Country"
# url = "https://en.wikipedia.org/wiki/Emotional"

driver.get(url)
heading = driver.find_element_by_id("firstHeading")


transitions = 0
visited_links = [driver.current_url]

while(heading.text != "Philosophy"):
    # content : WebElement = driver.find_element_by_id("mw-content-text")
    # paragraphs = driver.find_elements_by_xpath("/html/body/div[@id='content']/div[@id='bodyContent']/div[@id='mw-content-text']/div[@class='mw-parser-output']/p")
    # WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'p')))
    paragraphs = driver.find_element_by_id("mw-content-text").find_elements_by_xpath("//div[@class='mw-parser-output']/p")


    link : WebElement = None
    for p in paragraphs:
        links  = p.find_elements_by_tag_name("a")
        for l in links:
            parent : WebElement = l.find_element_by_xpath("..")
            if parent.tag_name == "i":
                continue
            elif l.text.startswith("[") and l.text.endswith("]"):
                continue
            elif is_in_parenthesis(p.text, p.text.find(l.text), "(", ")"):
                continue
            elif l.text == "":
                continue
            elif l.get_attribute("href") == None:
                continue
            elif not l.get_attribute("href").startswith("https://en.wikipedia.org"):
                continue
            else:
                link = l
                break
        if link != None:
            break

    if link == None:
        break
    
    
    if link.get_attribute("href") in visited_links:
        break
    link.click()
    # Simplest quickest solution
    time.sleep(1)
    visited_links.append(driver.current_url)
    transitions += 1
    heading = driver.find_element_by_id("firstHeading")

print("This application made {} transitions and visited folowing links: ".format(transitions))
print(visited_links)




