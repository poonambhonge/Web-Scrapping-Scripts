from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd

from bs4 import BeautifulSoup
import cchardet

import time


class RecipeScraping:
    def __init__(self):
        # put the name of the file in which you have all the links that you need to scrap
        with open("links_to_scrap.txt") as file:
            self.links = file.readlines()

    def scrapper(self, start, end):

        df = pd.DataFrame()
        sno = start
        undone_links = []
        for link in self.links[start:end]:

            try:
                print("Scraping Started.....")
                url = link
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                driver.minimize_window()

                # Searching the webpage
                driver.get(url)
                time.sleep(10)
                real_soup = BeautifulSoup(driver.page_source, "lxml")
                driver.quit()
                ab = real_soup.find_all("li", {"class": "diet_draggable"})

                # Scrapping the image
                image = real_soup.find_all('img')
                image_src = image[0].get('src')

                # Scapping ingradient name, measure, weight, and quantity.
                Ingredients_list = []
                food_name = []
                Measure = []
                Serving_Weight = []
                Quantity = []

                for i in ab:
                    a = i.find("div", {"class": "print_name"})
                    # print(a.text.strip())
                    food_name.append(a.text)
                    Ingredients_list.append(a.text)
                    b = i.find("div", {"class": "food_units col-12"})
                    # print(b.text.strip())
                    mea = b.text.strip()
                    mea = mea.split("(")
                    # print(mea[0])
                    Quantity.append(mea[0])
                    Ingredients_list.append(mea[0])
                    # print(mea[0])
                    Measure.append(mea[0])

                    # Intredients_list.append(mea[0])
                    c = i.find("div", {"class": "gram_printout col-12"})
                    # print(c.text.strip())
                    Serving_Weight.append(c.text.strip())
                    Ingredients_list.append(c.text.strip())

                # Scrapping Required time for Preparation and Cooking
                Required_Time = (
                    (real_soup.find("div", {"class": "row text-small text-medium-md"}))
                    .text.strip()
                    .replace("\n", "")
                )
                s = [int(i) for i in Required_Time.split() if i.isdigit()]
                Req_Time = " ".join(map(str, s)).replace(" ", ",")

                # print(Req_Time)

                # Scrapping title
                Title = real_soup.findAll("div", {"class": "modal-header"})
                for ti in Title:
                    temp = ti.find("h2")
                    Recipe_title = temp.text.strip()
                    # print(temp.text.strip())
                # Recipe_title=real_soup.find("div", {"class": "modal-title"})
                # print(Recipe_title)

                # Scrapping instructions to cook/prepare
                Instruction_to_cook = real_soup.find(
                    "div", {"class": "directions_list collection-list"}
                )
                # print(Instruction_to_cook.text)
                i = 0
                new_lst = []
                while i < len(Ingredients_list):
                    new_lst.append(Ingredients_list[i] + '-' + Ingredients_list[i + 1] + '-' + Ingredients_list[i + 2])
                    i += 3

                Ingredients_list = "|".join(new_lst)


                # creating dataframe
                df.loc[sno, "S.No"] = sno + 1
                df.loc[sno, "Link"] = link
                df.loc[sno, "Recipe_title"] = Recipe_title
                df.loc[sno, "Req_Time"] = Req_Time.replace("\t", "")
                df.loc[sno, "Instruction_to_cook"] = (
                    Instruction_to_cook.text.replace("\n", "")
                    .replace("Step 1 ", "Step-")
                    .replace("Step 2 ", "Step-")
                    .replace("Step 3 ", "Step-")
                    .replace("Step 4 ", "Step-")
                    .replace("Step 5 ", "Step-")
                    .replace("Step 6 ", "Step-")
                    .replace("Step 7 ", "Step-")
                    .replace("Step 8 ", "Step-")
                    .replace("Step 9 ", "Step-")
                    .replace("Step 10 ", "Step-")
                    .replace("Step 11 ", "Step-")
                    .replace("Step 12 ", "Step-")
                )
                df.loc[sno, "Ingredients_list"] = Ingredients_list
                df.loc[sno, "Image_src"] = image_src

                # Take care about this, its not "VEG" always
                # for i in self.df1["Category"]:
                #     diet_category = i
                diet_category = "Mediterranean"

                df.loc[sno, "Category"] = diet_category
                sno += 1
                print(f"Scrapping of link {sno-1} - Done!")
                print()

            except Exception as e:
                undone_links.append([link, Exception])
                print(f"This link wasn't scrapped due to some error {link}, Exception- {e}")
                continue

        # print(df)
        df.to_excel(r"results2.xlsx")
        if undone_links:
            print("Unable to scrap these links: \n")
            for link, exception in undone_links:
                print(link, "-", exception)

        return (
            f"Sccessfully scrapped and saved indexed {start} to {end - 1}!"
        )


obj = RecipeScraping()
print(obj.scrapper(400,420))
