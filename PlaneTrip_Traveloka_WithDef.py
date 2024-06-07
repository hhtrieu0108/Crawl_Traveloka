import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import datetime
import pandas as pd
import glob

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
            url.append(f"https://www.traveloka.com/vi-vn/flight/fullsearch?ap={place}&dt={day.strftime(format='%d-%m-%Y')}.NA&ps=1.0.0&sc=ECONOMY")
    return url

def crawl_planetrip(url_list):
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
                                    'start_time', 'start_day',
                                    'end_day', 'end_time',
                                    'trip_time', 'take_place', 'destination'])
        initial_page_length = driver.execute_script("return document.body.scrollHeight")
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
        scroll_step = initial_page_length // 200

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
            "//div[@class='css-1dbjc4n r-9nbb9w r-otx420 r-1i1ao36 r-1x4r79x']"
            )
        
        price_elements = wait.until(EC.visibility_of_all_elements_located((
            By.XPATH, 
            "//div[@class='css-1dbjc4n r-obd0qt r-eqz5dr r-1cmwbt1 r-knv0ih']" \
            "//h3[@class='css-4rbku5 css-901oao r-t1w4ow r-ubezar r-b88u0q r-rjixqe r-fdjqy7']"
            )))

        brand_elements = wait.until(EC.visibility_of_all_elements_located((
            By.XPATH, 
            "//div[@class='css-1dbjc4n r-1habvwh r-18u37iz r-1ssbvtb']//" \
            "div[@class='css-901oao css-cens5h r-t1w4ow r-ubezar r-majxgm r-135wba7 r-fdjqy7']"
            )))

        detail = wait.until(EC.visibility_of_all_elements_located((
            By.XPATH, 
            "//div[@class='css-1dbjc4n r-1awozwy r-1xr2vsu r-13awgt0 r-18u37iz r-1w6e6rj r-3mtglp r-1x4r79x']" \
            "//div[@class='css-901oao r-t1w4ow r-1b43r93 r-majxgm r-rjixqe r-fdjqy7']"
            )))

        for i, j in zip(range(len(elements)), detail[::4]):
            if elements[i] in old_element:
                continue
            ActionChains(driver).move_to_element(j).click().perform()
            
            old_element.append(elements[i])
            
            start_time_elements = wait.until(EC.visibility_of_element_located((
                By.XPATH, 
                "//div[@class='css-1dbjc4n r-e8mqni r-1d09ksm r-1h0z5md r-ttb5dx']" \
                "//div[@class='css-901oao r-t1w4ow r-1b43r93 r-majxgm r-rjixqe r-5oul0u r-fdjqy7']"
                )))

            start_time.append(start_time_elements.text)

            end_time_elements = wait.until(EC.visibility_of_element_located((
                By.XPATH, 
                "//div[@class='css-1dbjc4n r-e8mqni r-1d09ksm r-1h0z5md r-q3we1 r-ttb5dx']" \
                "//div[@class='css-901oao r-t1w4ow r-1b43r93 r-majxgm r-rjixqe r-fdjqy7']"
                )))

            end_time.append(end_time_elements.text)

            start_date_elements = wait.until(EC.visibility_of_element_located((
                By.XPATH, 
                "//div[@class='css-1dbjc4n r-e8mqni r-1d09ksm r-1h0z5md r-ttb5dx']" \
                "//div[@class='css-901oao r-t1w4ow r-1enofrn r-majxgm r-1cwl3u0 r-fdjqy7']"
                )))
            start_day.append(start_date_elements.text)

            end_date_elements = wait.until(EC.visibility_of_element_located((
                By.XPATH, 
                "//div[@class='css-1dbjc4n r-e8mqni r-1d09ksm r-1h0z5md r-q3we1 r-ttb5dx']" \
                "//div[@class='css-901oao r-t1w4ow r-1enofrn r-majxgm r-1cwl3u0 r-fdjqy7']"
                )))

            end_day.append(end_date_elements.text)

            trip_time_elements = wait.until(EC.visibility_of_element_located((
                By.XPATH, 
                "//div[@class='css-901oao r-13awgt0 r-t1w4ow r-1enofrn r-majxgm r-1cwl3u0 r-fdjqy7']"
                )))
            trip_time.append(trip_time_elements.text)

            destination_elements = wait.until(EC.visibility_of_element_located((
                By.XPATH,
                "//div[@class='css-1dbjc4n r-e8mqni r-1habvwh r-13awgt0 r-1h0z5md r-q3we1']"
                )))
            destination.append(destination_elements.text)

            take_place_elements = wait.until(EC.visibility_of_element_located((
                By.XPATH, 
                "//div[@class='css-1dbjc4n r-e8mqni r-1habvwh r-13awgt0 r-1h0z5md']"
                )))
            take_place.append(take_place_elements.text)

            price.append(price_elements[i].text)

            brand.append(brand_elements[i].text)
            new_df = pd.DataFrame(list(zip(brand, price,
                                            start_time,
                                            start_day, end_time, end_day,
                                            trip_time, take_place, destination)),
                                    columns=['brand', 'price',
                                            'start_time',
                                            'start_day', 'end_time', 'end_day',
                                            'trip_time', 'take_place', 'destination'])

            df = pd.concat((df, new_df), axis=0, ignore_index=True)
            start_time = []
            end_time = []
            start_day = []
            end_day = []
            trip_time = []
            take_place = []
            destination = []
            price = []
            brand = []
            j.click()
            sleep(1)
        new_url = url[53:]
        df.to_csv(f"Planetrip_{new_url}.csv", index=False)
        df_by_url[new_url] = df
    driver.quit()
    return df_by_url

def preprocessing_data(df_by_url):
    process_data = {}
    for url, data in zip(df_by_url.keys(), df_by_url.values()):
        new_data = data.copy()
        new_data['price'] = new_data['price'].str.split(' ').str[0].str.replace('.', '').astype('int64')
        new_data['end_day'] = new_data['end_day'].str.split(' ').str[0] + '-' + \
            new_data['end_day'].str.split(' ').str[1].replace(
            {"Jan": '01', "Feb": '02', "Mar": '03',
                "Apr": '04', "May": '05', "Jun": '06',
                "Jul": '07', "Aug": '08', "Sep": '09',
                "Oct": '10', "Nov": '11', "Dec": '12'}) + '-' + str(datetime.datetime.today().year)
        new_data['start_day'] = new_data['start_day'].str.split(' ').str[0] + '-' + \
            new_data['start_day'].str.split(' ').str[1].replace(
            {"Jan": '01', "Feb": '02', "Mar": '03',
                "Apr": '04', "May": '05', "Jun": '06',
                "Jul": '07', "Aug": '08', "Sep": '09',
                "Oct": '10', "Nov": '11', "Dec": '12'}) + '-' + str(datetime.datetime.today().year)

        new_data.to_csv(f"Processed_Data_PlaneTrip/PlaneTrip_{url}.csv", index=False)
        process_data[url] = new_data

def last_processing():
    """
    :return: Full data with full information
    """
    csv_file = glob.glob("Processed_Data_PlaneTrip/*.csv")
    full_data = pd.read_csv("Processed_Data_PlaneTrip/PlaneTrip_SGN.CXR&dt=20-05-2024.NA&ps=1.0.0&sc=ECONOMY.csv")
    full_data['trip_to'] = 'Nha Trang'
    today = datetime.datetime.today().date()
    next_day = today + datetime.timedelta(days=4)
    for data in csv_file[1:5]:
        df = pd.read_csv(data)
        df['trip_to'] = 'Nha Trang'
        full_data = pd.concat((full_data, df), axis=0, ignore_index=True)
    for data in csv_file[5:10]:
        df = pd.read_csv(data)
        df['trip_to'] = 'Đà Nẵng'
        full_data = pd.concat((full_data, df), axis=0, ignore_index=True)
    full_data['id'] = np.arange(1, len(full_data) + 1)
    full_data.to_csv(f"Processed_Data_PlaneTrip/PlaneTrip_Full_{today.strftime(format='%d-%m-%Y')}_\
                                                                {next_day.strftime(format='%d-%m-%Y')}.csv", 
                                                                index=False)
    return full_data

if __name__ == "__main__":
    places = ['SGN.DAD','SGN.CXR']

    url_list = get_url(places)
    df_by_url = crawl_planetrip(url_list)
    process_data = preprocessing_data(df_by_url)
    last_processing()