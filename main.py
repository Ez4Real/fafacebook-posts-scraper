import pandas as pd

from time import sleep, time

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from bs4 import BeautifulSoup


def get_posts():
    return posts_con.find_elements(By.XPATH,
                                   './/*[contains(@class, "x1yztbdb") and \
                                         contains(@class, "x1n2onr6") and \
                                         contains(@class, "xh8yej3") and \
                                         contains(@class, "x1ja2u2z")]'
                                    )


options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("start-maximized")
options.add_argument("--disable-notifications")
options.add_argument("--lang=en")

name_list = []
profile_list = []
content_list = []
images_list = []

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(options=options, service=service)

driver.get('https://www.facebook.com/groups/407875615934797')
# SLEEP
sleep(2)

posts_con = driver.find_element(By.XPATH, '//div[@role="feed"]')
sleep(1)

start_time = time()

posts = get_posts()

current_post_index = 0

while current_post_index < 724:
    print('\n\nPost index:', current_post_index)
    current_post = posts[current_post_index]
    driver.execute_script("arguments[0].scrollIntoView();", current_post)
    sleep(1)

    try:
        see_more_el = driver.find_element(By.XPATH, '//div[contains(@class, "x1i10hfl") and text()="See more"]')
        see_more_el.click()
    except:
        print('No See more btn')

    post_html = current_post.get_attribute('outerHTML')
    soup = BeautifulSoup(post_html, 'html.parser')
    sleep(1)
    
    try:
        name = soup.find('strong').text
    except:
        name = "Name not found"
    print('Name:', name)

    try:
        profile_url = soup.find_all('a')[2].get('href')
    except:
        profile_url = "Profile url not found"
    print('Profile link:', profile_url)

    try:
        content_child = soup.find('div', class_='', dir='auto')
        content = content_child.parent.get_text()
    except:
        content = "Content Element not found."

    print('\nContent:', content)

    try:
        image_tags = soup.find_all("img", class_=["x1ey2m1c", "xds687c", "x5yr21d", "x10l6tqk", "x17qophe", "x13vifvy", "xh8yej3"])
        images = [img["src"] for img in image_tags]
    except:
        images = "No images in post"

    print('\nImages:', images)

    name_list.append(name)
    profile_list.append(profile_url)
    content_list.append(content)
    images_list.append(images)

    # Find new posts
    new_posts = get_posts()
    posts = new_posts
    current_post_index += 1


# Execution
end_time = time()
execution_time = end_time - start_time
print("\nScript execution time: ", execution_time, " seconds")

df = pd.DataFrame({
    "name": name_list,
    "profile_url": profile_list,
    "content": content_list,
    "images": images_list,
})
df.to_csv("SFIntComA.csv")