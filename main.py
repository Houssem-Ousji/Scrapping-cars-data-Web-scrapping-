from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
print(cars_list)

# Making Directories of such brand and Download all the logos
# creating file contain list of all brands
car_file = open("Scrapping-cars-data-Web-scrapping-\list of cars.txt", "w")
for car in cars_list:
    car_brand = car[1][:-5]
    car_file.write(car_brand+'\n')
    os.mkdir('Scrapping-cars-data-Web-scrapping-\{}'.format(car_brand))
    urllib.request.urlretrieve(url = car[0], filename = 'Scrapping-cars-data-Web-scrapping-\{}\{}.png'.format(car_brand, car[1]))



