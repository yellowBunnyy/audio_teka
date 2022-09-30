from selenium import webdriver
import chromedriver_binary
import time

# https://medium.com/analytics-vidhya/using-python-and-selenium-to-scrape-infinite-scroll-web-pages-825d12c24ec7
driver = webdriver.Chrome()

my_url = "https://web.audioteka.com/pl/do-uslyszenia-w-klubie.html"
driver.get(my_url)
time.sleep(2)
scroll_pause_time = 5
screen_height = driver.execute_script("return window.screen.height;")
i = 0
print(screen_height)


while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    print(i,f" Wielkość ekranu: {screen_height * i}, {scroll_height}")
    if (screen_height) * i > scroll_height + screen_height:
        break
print(f"summary counter: {i}")



with open("audioteka_new.html", "w") as f:
    f.write(driver.page_source)
    f.write(f"summary counter: {i}")

driver.close()