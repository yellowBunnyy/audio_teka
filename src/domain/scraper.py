from selenium import webdriver
import chromedriver_binary
import time

SCROLL_PAUSE = 5


def get_driver(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)
    return driver


def scroll_down_page(driver, counter):
    screen_height = get_screen_height(driver)
    driver.execute_script(
        "window.scrollTo(0, {screen_height}*{i});".format(
            screen_height=screen_height, i=counter
        )
    )
    time.sleep(SCROLL_PAUSE)
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    print(counter, f" Screan height: {screen_height * counter}, {scroll_height}")
    if (screen_height) * counter > scroll_height + screen_height:
        return True


def get_screen_height(driver):
    return driver.execute_script("return window.screen.height;")


def save_data_to_file(driver):
    with open("audioteka_new.html", "w") as f:
        f.write(driver.page_source)


def main():
    my_url = "https://web.audioteka.com/pl/do-uslyszenia-w-klubie.html"
    driver = get_driver(my_url)
    counter = 0
    print(f"Screan height: {get_screen_height(driver)}")
    while True:
        if scroll_down_page(driver, counter):
            break
        counter += 1
    save_data_to_file(driver)
    driver.close()


if __name__ == "__main__":
    main()
