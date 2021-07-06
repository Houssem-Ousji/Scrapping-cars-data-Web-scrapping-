# import libraries and Classes
from selenium import webdriver
import os
import urllib.request

driver = webdriver.Chrome("C:\Program Files\chromedriver.exe") #Put the path of Your webdriver

def get_source():
    cars_list = []
    for i in range(1, 2):
        page = "https://www.carlogos.org/car-brands/list_1_{}.html".format(i)
        driver.get(page)
        cars = driver.find_element_by_class_name('logo-list')
        cars_links = cars.find_elements_by_tag_name('a')
        cars_logos = cars.find_elements_by_tag_name('img')
        for j in range(len(cars_links)):
            car_data = []
            car_data.append(cars_links[j].get_attribute('href'))
            car_data.append(cars_logos[j].get_attribute('src'))
            cars_list.append(car_data)
    return (cars_list)

def clean_car_data(data):
    clean_data = []
    data_lines = data.split('\n')
    for x in data_lines:
        if x.count('<') != 1 and  x != '':
            y = ''
            test = False
            while test == False:
                x = x[x.index('>')+1:]
                if len(x) == 0:
                    test = True
                elif x[0] != '<':
                    if len(y) == 0:
                        y += x[:x.index('<')]
                    else:
                        y += ' '+ x[:x.index('<')]
            clean_data.append(y)
    return (clean_data)

def get_data(cars_list):
    car_file = open("list of cars.txt", "w")
    car_file.write('The list of cars: \n')
    print("Start Scrapp the data of {} brands: ".format(len(cars_list)))
    for car in cars_list:
        driver.get(car[0])
        car_brand = driver.find_element_by_class_name('title').find_element_by_tag_name('h1').get_attribute('innerHTML')
        car_brand = car_brand[:-5]
        print("{}.Srapp the data of {}".format(cars_list.index(car), car_brand))
        if car_brand[-1] == ' ':
            car_brand = car_brand[:car_brand.rindex(' ')]
        try:
            car_information = driver.find_element_by_class_name('brand-overview').find_element_by_class_name(
                'fold-text').get_attribute('innerHTML')
        except:
            car_information = driver.find_element_by_tag_name('tbody').get_attribute('innerHTML')
        car_information = clean_car_data(car_information)
        os.mkdir('{}'.format(car_brand))
        urllib.request.urlretrieve(url=car[1], filename='{}\{}.png'.format(car_brand, car_brand + ' Logo'))
        car_data_file = open('{}\{}.txt'.format(car_brand, car_brand + ' Review'), 'w')
        test_2 = True
        for line in car_information:
            if test_2:
                try:
                    car_data_file.write(line + '\n')
                except:
                    car_data_file.write('invalid data')
                    test_2 = False
        car_file.write('{}\n'.format(car_brand))
    driver.quit()
print("Be Patient...")
cars_list = get_source()
get_data(cars_list)
print("Done !")