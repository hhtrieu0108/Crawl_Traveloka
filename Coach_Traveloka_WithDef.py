"""
@author : hhtrieu0108
"""

import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import datetime
import pandas as pd

def get_url(places):
    """
    :param places: list_of_place base on url of traveloka coach
    :return: list of url
    """
    url = []
    date = []
    today = datetime.datetime.today().date()
    date.append(today)
    for i in range(1,5):
        date.append(today + datetime.timedelta(days=i))
    for place in places:
        for day in date:
            url.append(f"https://www.traveloka.com/vi-vn/bus-and-shuttle/search?st=a10009794.{place}dt={day.strftime(format='%d-%m-%Y')}.null&ps=1")
    return url

def crawl_coach(url_list):
    """
    :param url_list: list of url
    :return: dictionary with key is url and value is dataframe
    """
    df_by_url = {}
    driver = webdriver.Edge()
    for url in url_list:
        driver.get(url)
        sleep(5)
        wait = WebDriverWait(driver, 50)
        df = pd.DataFrame(columns=['brand', 'price',
                                    'number_of_seat', 'start_time',
                                    'start_day', 'end_day', 'end_time',
                                    'trip_time', 'take_place', 'destination'])
        initial_page_length = driver.execute_script("return document.body.scrollHeight")
        number_of_seat = []
        type_of_seat = []
        start_time = []
        end_time = []
        start_day = []
        end_day = []
        trip_time = []
        take_place = []
        destination = []
        price = []
        brand = []
        num_steps = 1000000
        scroll_step = initial_page_length // 500

        old_element = []
        for i in range(num_steps):

            scroll_position = scroll_step * (i + 1)

            driver.execute_script(f"window.scrollTo(0, {scroll_position});")
            position = driver.execute_script("return window.scrollY")
            new_height = driver.execute_script("return document.body.scrollHeight")

            if scroll_position >= new_height:
                break

        driver.execute_script("window.scrollTo(0, 0)")
        elements = driver.find_elements(
            By.XPATH,
            "//div[@class='css-1dbjc4n r-14lw9ot r-kdyh1x r-da5iq2 r-5oul0u r-1udh08x r-16yfudc']"
            )

        price_elements = wait.until(EC.visibility_of_all_elements_located((
            By.XPATH, 
            "//div[@class='css-1dbjc4n r-14lw9ot r-kdyh1x r-da5iq2 r-5oul0u r-1udh08x r-16yfudc']" \
            "//h2[@class='css-4rbku5 css-901oao r-t1w4ow r-adyw6z r-b88u0q r-135wba7 r-fdjqy7']"
            )))

        brand_elements = wait.until(EC.visibility_of_all_elements_located((
            By.XPATH, 
            "//div[@class='css-1dbjc4n r-14lw9ot r-kdyh1x r-da5iq2 r-5oul0u r-1udh08x r-16yfudc']//" \
            "h3[@class='css-4rbku5 css-901oao r-t1w4ow r-ubezar r-b88u0q r-rjixqe r-fdjqy7']"
            )))

        roads = wait.until(EC.visibility_of_all_elements_located((
            By.XPATH, 
            "//div[@class='css-1dbjc4n r-1loqt21 r-w0va4e r-1otgn73 r-1i6wzkk r-lrvibr']" \
            "//h4[@class='css-4rbku5 css-901oao r-t1w4ow r-1b43r93 r-b88u0q r-1cwl3u0 r-fdjqy7']"
            )))

        for i, j in zip(range(len(elements)), roads[1::3]):
            if elements[i] in old_element:
                continue
            driver.execute_script("arguments[0].scrollIntoView(true);", j)
            elements[i].click()
            old_element.append(elements[i])

            seat = wait.until(EC.visibility_of_all_elements_located(
                (By.XPATH, "//div[@class='css-901oao r-t1w4ow r-1b43r93 r-b88u0q r-rjixqe r-15zivkp r-fdjqy7']")))

            if len(seat) == 4:
                number_of_seat.append(seat[1].text)
            if len(seat) == 3:
                number_of_seat.append(seat[0].text)
            if len(seat) == 4:
                number_of_seat.append(seat[2].text)
            if len(seat) == 3:
                number_of_seat.append(seat[1].text)
            j.click()
            time_elements = wait.until(EC.visibility_of_all_elements_located(
                (By.XPATH, "//div[@class='css-901oao r-t1w4ow r-1b43r93 r-b88u0q r-rjixqe r-1kb76zh r-fdjqy7 r-7bouqp']")))

            start_time.append(time_elements[0].text)
            end_time.append(time_elements[1].text)

            day_elements = wait.until(EC.visibility_of_all_elements_located(
                (By.XPATH, "//div[@class='css-901oao r-t1w4ow r-1enofrn r-b88u0q r-1cwl3u0 r-1kb76zh r-fdjqy7 r-7bouqp']")))

            start_day.append(day_elements[0].text)
            end_day.append(day_elements[1].text)

            trip_time_elements = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='css-901oao r-13awgt0 r-t1w4ow r-1enofrn r-majxgm r-1cwl3u0 r-fdjqy7']")))

            trip_time.append(trip_time_elements.text)

            place = wait.until(EC.visibility_of_all_elements_located(
                (By.XPATH, "//div[@class='css-1dbjc4n r-e8mqni r-1habvwh r-13awgt0 r-1h0z5md']")))

            take_place.append(place[0].text + ' ' + place[1].text)
            destination.append(place[2].text + ' ' + place[3].text)

            price.append(price_elements[i].text)

            brand.append(brand_elements[i].text)

            driver.execute_script("arguments[0].scrollIntoView(true);", j)
            j.click()

            new_df = pd.DataFrame(list(zip(brand, price,
                                            number_of_seat, start_time,
                                            start_day, end_time, end_day,
                                            trip_time, take_place, destination)),
                                    columns=['brand', 'price',
                                            'number_of_seat', 'start_time',
                                            'start_day', 'end_time', 'end_day',
                                            'trip_time', 'take_place', 'destination'])
            df = pd.concat((df, new_df), axis=0, ignore_index=True)

            number_of_seat = []
            type_of_seat = []
            start_time = []
            end_time = []
            start_day = []
            end_day = []
            trip_time = []
            take_place = []
            destination = []
            price = []
            brand = []

        new_url = url[68:]
        df.to_csv(f"Planetrip_{new_url}.csv", index=False)
        df_by_url[new_url] = df
    driver.quit()
    return df_by_url

def preprocessing_data(df_by_url):
    """
    :param df_by_url: dataframe by url
    :return: processed dataframe
    """
    process_data = {}
    for url,data in zip(df_by_url.keys(),df_by_url.values()):
        new_data = data.copy()
        new_url = url[68:]

        new_data['price'] = new_data['price'].str.split(' ').str[0].str.replace('.', '').astype('int64')

        new_data['number_of_seat'] = (new_data['number_of_seat'].str.split(' ').str[2] + ' ' +
                                    new_data['number_of_seat'].str.split(' ').str[3] + ' ' +
                                    new_data['number_of_seat'].str.split(' ').str[4])
        if datetime.datetime.today().month < 10:
            new_data['start_day'] = new_data['start_day'].str.split(' thg').str[0] + '-' + '0' + \
                                    str(datetime.datetime.today().month) + '-' + \
                                    str(datetime.datetime.today().year)

            new_data['end_day'] = new_data['end_day'].str.split(' thg').str[0] + '-' + '0' + \
                                str(datetime.datetime.today().month) + '-' + \
                                str(datetime.datetime.today().year)

        elif datetime.datetime.today().month >= 10:
            new_data['start_day'] = new_data['start_day'].str.split(' thg').str[0] + '-' + \
                                    str(datetime.datetime.today().month) + '-' + \
                                    str(datetime.datetime.today().year)

            new_data['end_day'] = data['end_day'].str.split(' thg').str[0] + '-' + \
                                str(datetime.datetime.today().month) + '-' + \
                                str(datetime.datetime.today().year)

        new_data['trip_time'] = new_data['trip_time'].str.replace('giờ', ' giờ').str.replace('phút', ' phút')

        new_data['id'] = np.arange(1,len(new_data)+1)

        new_data.to_csv(f"Processed_Data_PlaneTrip/PlaneTrip_{new_url}.csv",index=False)

        process_data[new_url] = new_data

if __name__ == "__main__":
    places = ['a10010498&stt=CITY_GEO.CITY_GEO&stn=Ho%20Chi%20Minh%20City.Nha%20Trang&',
                'a10010083&stt=CITY_GEO.CITY_GEO&stn=Ho%20Chi%20Minh%20City.%C4%90%C3%A0%20N%E1%BA%B5ng&',
                'a10009889&stt=CITY_GEO.CITY_GEO&stn=Ho%20Chi%20Minh%20City.Ba%20Ria%20-%20Vung%20Tau&']

    url_list = get_url(places)
    df_by_url = crawl_coach(url_list)
    process_data = preprocessing_data(df_by_url)
