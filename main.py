from selenium import webdriver
from time import process_time
import os
import urllib.request

driver = webdriver.Chrome("C:\Program Files\chromedriver.exe")


# getting the data (src and name of the logo and his link)
cars_list = []
for i in range(1, 2):
   page = "https://www.carlogos.org/car-brands/list_1_{}.html".format(i)
   driver.get(page)
   cars = driver.find_element_by_class_name('logo-list')
   car_links = cars.find_elements_by_tag_name('a')
   cars_images = driver.find_elements_by_tag_name('img')
   j = 0
   for image in cars_images:
       if j < len(car_links):
           cars_data = []
           cars_data.append(image.get_attribute('src'))
           cars_data.append(image.get_attribute('alt'))
           cars_data.append(car_links[j].get_attribute('href'))
           if cars_data not in cars_list:
               cars_list.append(cars_data)
           j += 1

# Making Directories of such brand and Download all the logos
# creating file contain list of all brands
car_file = open("list of cars.txt", "w")
for car in cars_list:
    car_brand = car[1][:-5]
    car_file.write(car_brand+'\n')
    os.mkdir('{}'.format(car_brand))
    urllib.request.urlretrieve(url = car[0], filename = '{}\{}.png'.format(car_brand, car[1]))


def clean_car_data(data):
    data_lines = []
    clean_data = []
    for x in data:
        if x == '\n':
            data_lines.append(data[:data.index(x)])
            data = data[data.index(x)+1:]
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

# Downloading All the Brands Review
for car_link in cars_list:
    driver.get(car_link[2])
    car_title = driver.find_element_by_class_name('title').find_element_by_tag_name('h1').get_attribute('innerHTML')
    car_title = car_title[:-5]
    try:
        car_information = driver.find_element_by_class_name('brand-overview').find_element_by_class_name(
            'fold-text').get_attribute('innerHTML')
    except:
        car_information = driver.find_element_by_tag_name('tbody').get_attribute('innerHTML')

    car_data = clean_car_data(car_information)
    car_data_file = open('{}\{}.txt'.format(car_title, car_title + ' data'), 'w')
    for x in car_data:
        try:
            car_data_file.write(x + '\n')
        except:
            car_data_file.write('invalid data')

print("scrapping the data takes: ".format(process_time()))

