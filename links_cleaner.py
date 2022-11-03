import pandas as pd


def clean_links():
    xls = pd.ExcelFile(
        r"D:\Intershala projects\Blackcoffer\Input.xlsx"
    )  # put your file address here.

    df1 = pd.read_excel(xls, "Sheet1")  # add the sheet name here.
    links = set()

    for link in df1["URL"]:
        try:
            links.add(link)
        except:
            continue

    links = list(links)
    return links


def create_file(link_lst):
    file = open("links_to_scrap.txt", "a")
    for link in link_lst:
        file.write(link)
        file.write("\n")
    file.close()
    print("Created a file named 'links_to_scrap' and saved all the links in it.")
    return


links_to_scrap = clean_links()
create_file(links_to_scrap)