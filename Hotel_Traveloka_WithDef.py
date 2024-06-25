"""
@author : hhtrieu0108
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import datetime
import pandas as pd
import numpy as np

def process_rating(x):
    if x == 'No value':
        return x
    elif x == 'Chưa có đánh giá nào':
        return "No value"
    else:
        return x.split(' ')[3].replace('.', '')

def process_price(x):
    if x == 'No value':
        return x
    else:
        return x.split(' ')[0].replace('.', '')

def process_score(x):
    if x == '-':
        return "No value"
    else:
        return x

def get_url(list_of_places):
    """
    :param list_of_places: list of place you want to crawl. But need to take from url of traveloka
    :return: list of url from traveloka
    """
    list_of_url = []
    time = datetime.datetime.today().date()
    next_time = time + datetime.timedelta(days=1)
    for place in list_of_places:
        url = f"https://www.traveloka.com/vi-vn/hotel/search?spec={time.strftime(format='%d-%m-%Y')}.{next_time.strftime(format='%d-%m-%Y')}.1.1.HOTEL_GEO.{place}.1"
        list_of_url.append(url)
    return list_of_url

def crawl_data(list_of_url,list_of_places):
    """
    :param list_of_url: Url of the traveloka web
    :return: dataframe in csv file and dictionary of dataframe with key is place and value is dataframe
    """
    driver = webdriver.Edge()
    hotel_by_place = {}

    for url,place in zip(list_of_url,list_of_places):
        driver.get(url)
        sleep(10)

        current_window = driver.current_window_handle

        def get_hotels():
            return driver.find_elements(By.XPATH, "//div[@class='css-1dbjc4n'][@data-testid='tvat-searchListItem']")

        df_traveloka = pd.DataFrame(columns=['hotel_names', 'location', 'price', 'score_hotels',
                                                'number_rating', 'star_number', 'received_time',
                                                'giveback_time', 'description', 'hotel_link'])
        list_hotel_exist = []
        hotel_names = []
        location_texts = []
        price_text = []
        description_text = []
        star_number_texts = []
        hotel_link = []
        score_hotels = []
        number_rating_text = []
        received_time = []
        giveback_time = []
        num_steps = 5000
        while True:

            previous_scroll_position = driver.execute_script("return window.scrollY")

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

            sleep(2)

            new_scroll_position = driver.execute_script("return window.scrollY")

            if new_scroll_position <= previous_scroll_position:
                break

        driver.execute_script("window.scrollTo(0, 0)")

        for step in range(num_steps):
            current_position = driver.execute_script("return window.scrollY")
            if current_position == new_scroll_position:
                break
            try:
                list_hotel = get_hotels()
                for index in range(len(list_hotel)):
                    if list_hotel[index] in list_hotel_exist:
                        continue

                    ActionChains(driver).move_to_element(list_hotel[index]).click().perform()

                    list_hotel_exist.append(list_hotel[index])

                    driver.switch_to.window(driver.window_handles[1])

                    wait_time = 10

                    try:
                        hotel_name_elements = WebDriverWait(driver, wait_time).until(
                            EC.visibility_of_all_elements_located((
                                By.XPATH,
                                "//h1[@class='css-4rbku5 css-901oao css-cens5h r-cwxd7f r-t1w4ow r-1ui5ee8 r-b88u0q r-nwxazl r-fdjqy7']"))
                        )
                    except:
                        print("Error hotel")
                        print("Link: ", driver.current_url)
                        print(hotel_name_elements)

                        try:
                            hotel_name_elements = WebDriverWait(driver, wait_time).until(
                                EC.visibility_of_all_elements_located((
                                    By.XPATH,
                                    "//h1[@class='css-4rbku5 css-901oao css-cens5h r-t1w4ow r-1ui5ee8 r-b88u0q r-nwxazl r-fdjqy7']"))
                            )
                        except:
                            print("Error hotel 2")
                            print("Link: ", driver.current_url)

                    try:
                        location_elements = WebDriverWait(driver, wait_time).until(
                            EC.visibility_of_all_elements_located((
                                By.XPATH,
                                "//div[@class='css-901oao css-cens5h r-cwxd7f r-13awgt0 r-t1w4ow r-1b43r93 r-majxgm r-rjixqe r-fdjqy7']"))
                        )
                    except:
                        print("Error location")
                        print("Link: ", driver.current_url)

                        try:
                            location_elements = WebDriverWait(driver, wait_time).until(
                                EC.visibility_of_all_elements_located((
                                    By.XPATH,
                                    "//div[@class='css-901oao css-cens5h r-13awgt0 r-t1w4ow r-1b43r93 r-majxgm r-rjixqe r-fdjqy7']"))
                            )
                        except:
                            print("Error location 2")
                            print("Link: ", driver.current_url)

                    try:
                        price_elements = WebDriverWait(driver, wait_time).until(
                            EC.visibility_of_all_elements_located((
                                By.XPATH, 
                                "//div[@class='css-901oao r-t1w4ow r-1x35g6 r-b88u0q r-vrz42v r-fdjqy7']"))
                        )
                    except:
                        print("Error in price")
                        print("Link: ", driver.current_url)

                    try:
                        star_number = WebDriverWait(driver, wait_time).until(
                            EC.visibility_of_all_elements_located((
                                By.XPATH,
                                "//div[@class='css-1dbjc4n']//div[@class='css-1dbjc4n r-18u37iz']//div[@class='css-1dbjc4n r-18u37iz']"))
                        )
                    except:
                        print("Error in star number")
                        print("Link: ", driver.current_url)

                    try:
                        score = WebDriverWait(driver, wait_time).until(
                            EC.visibility_of_all_elements_located((
                                By.XPATH,
                                "//div[@class='css-901oao r-jwli3a r-t1w4ow r-adyw6z r-b88u0q r-135wba7 r-fdjqy7']"))
                        )
                    except:
                        print("Error in score")
                        print("Link: ", driver.current_url)

                    try:
                        number_rating = WebDriverWait(driver, wait_time).until(
                            EC.visibility_of_all_elements_located((
                                By.XPATH,
                                "//div[@class='css-901oao r-jwli3a r-t1w4ow r-1enofrn r-b88u0q r-1cwl3u0 r-fdjqy7']"))
                        )
                    except:
                        print("Error in rating")
                        print("Link: ", driver.current_url)

                    try:
                        time = WebDriverWait(driver, wait_time).until(
                            EC.visibility_of_all_elements_located((
                                By.XPATH,
                                "//div[@class='css-901oao r-1h9nbw7 r-t1w4ow r-1b43r93 r-b88u0q r-rjixqe r-fdjqy7']"))
                        )
                    except:
                        print("Error in time")
                        print("Link: ", driver.current_url)

                    try:
                        for hotel_name_element in hotel_name_elements:
                            hotel_names.append(hotel_name_element.text)
                    except:
                        print("Error occurred while retrieving hotel names")

                    try:
                        for location_element in location_elements:
                            location_texts.append(location_element.text.split('\n')[0])
                    except:
                        print("Error location")

                    try:
                        for original_price_element in price_elements:
                            price_text.append(original_price_element.text)
                    except:
                        print("Error in price")

                    try:
                        for star_number_element in star_number:
                            star_number_texts.append(len(star_number_element.find_elements(By.TAG_NAME, "img")))
                    except:
                        print("Error star")

                    try:
                        for rating in number_rating:
                            number_rating_text.append(rating.text)
                    except:
                        print("Error in rating")

                    try:
                        for score_hotel in score:
                            score_hotels.append(score_hotel.text)
                    except:
                        print("Error in score")

                    try:
                        for received in time[::2]:
                            received_time.append(received.text)
                    except:
                        print("Error in received")

                    try:
                        for giveback in time[1::2]:
                            giveback_time.append(giveback.text)
                    except:
                        print("Error in giveback")

                    try:
                        hotel_link.append(driver.current_url)
                    except:
                        print("Error in link")

                    driver.execute_script(f"window.scrollTo(0, 20);")

                    try:
                        description_hotel = WebDriverWait(driver, wait_time).until(
                            EC.visibility_of_element_located((
                                By.XPATH,
                                "//div[@class='css-18t94o4 css-1dbjc4n r-kdyh1x r-1loqt21 r-10paoce r-5njf8e r-1otgn73 r-lrvibr']"))
                        )
                    except:
                        print("Error in button")

                    description_hotel.click()

                    detail_description = WebDriverWait(driver, wait_time).until(
                        EC.visibility_of_all_elements_located((
                            By.XPATH,
                            "//div[@class='css-1dbjc4n r-13awgt0 r-1rnoaur']//div[@class='css-1dbjc4n r-f4gmv6 r-nsbfu8']"))
                    )

                    for description in detail_description:
                        description_text.append(description.text)

                    driver.close()

                    driver.switch_to.window(current_window)
                    for check in [hotel_names, location_texts, price_text, 
                                    score_hotels, number_rating_text,star_number_texts,
                                    received_time, giveback_time, description_text, hotel_link]:
                        if check == []:
                            check.append("No value")

                    df_traveloka_new = pd.DataFrame(list(zip(hotel_names, location_texts, price_text,
                                                                score_hotels, number_rating_text, star_number_texts,
                                                                received_time, giveback_time, description_text, hotel_link)),
                                                    columns=['hotel_names', 'location', 'price', 'score_hotels',
                                                                'number_rating', 'star_number', 'received_time',
                                                                'giveback_time', 'description', 'hotel_link'])

                    df_traveloka = pd.concat((df_traveloka, df_traveloka_new), axis=0, ignore_index=True)

                    hotel_names = []
                    location_texts = []
                    price_text = []
                    description_text = []
                    star_number_texts = []
                    hotel_link = []
                    score_hotels = []
                    number_rating_text = []
                    received_time = []
                    giveback_time = []

            except Exception as e:
                print("Error:", e)
                print(driver.current_url)

        df_traveloka_nodup = df_traveloka.drop_duplicates('hotel_names').reset_index(drop=True)
        hotel_by_place[place] = df_traveloka_nodup
        hotel_by_place[place].to_csv(f"Hotel_{place}_Traveloka.csv",index=False)
    driver.quit()
    return hotel_by_place

def processing_data(list_of_dataframe):
    """
    :param list_of_dataframe: list of dataframe with key is place and value is dataframe
    :return: processed dataframe in csv file
    """
    processed_hotel = {}
    for place,data in zip(list_of_dataframe.keys(),list_of_dataframe.values()):
        data['number_rating'] = data['number_rating'].apply(process_rating)
        
        data['price'] = data['price'].apply(process_price)
        
        data['score_hotels'] = data['score_hotels'].apply(process_score)
        
        data['id'] = np.arange(1, len(data) + 1)
        
        data.to_csv(f"Processed_Data/Hotel_{place}_Processed.csv",index=False)
        
        processed_hotel[place] = data
    return processed_hotel

if __name__ == "__main__":

    list_of_places = ['10010498.Nha%20Trang','10009888.Thành%20phố%20Vũng%20Tàu',
                        '10010083.Đà%20Nẵng','10009843.Hà%20Nội','10009794.Thành%20phố%20Hồ%20Chí%20Minh']

    list_of_url = get_url(list_of_places)
    hotel_by_place = crawl_data(list_of_places=list_of_places,list_of_url=list_of_url)
    processing_hotel = processing_data(list_of_dataframe=hotel_by_place)

