import csv
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import re

def remove_frequency(input_string):
    # Sử dụng regular expression để tìm và thay thế phần tần số bằng chuỗi trống
    output_string = re.sub(r'\s*\d+(\.\d+)?GHz\s*', '', input_string)
    return output_string
def remove_cpu_and_suffix(string):
    pattern = r"\s+(i3|i5|i7|i9|I3|I5|I7|I9|R3|R5|R7|R9).*$"
    result = re.sub(pattern, "", string)
    return result.strip()
driver = webdriver.Chrome(ChromeDriverManager().install())

a = []
id = 0
driver.get("https://www.thegioididong.com/laptop#c=44&o=17&pi=11")
laptop_card = driver.find_elements(By.CSS_SELECTOR, 'li[class=" item  __cate_44"] ')

for laptop in laptop_card:
    laptopLink = laptop.find_element(By.CSS_SELECTOR, "a.main-contain").get_attribute(
        "href"
    )

    a.append(laptopLink)


laptop_info = []
driver.implicitly_wait(20)
for link in a:
    id += 1
    if id > 0:
        driver.get(link)

        try:
            name = (
                driver.find_element(
                    By.CSS_SELECTOR,
                    'section[class="detail "] h1',
                )
                .text.split("/")[0]
                .replace("Laptop", "")
                .strip()
                .upper()
            )
        except:
            name = "https://www.thegioididong.com/laptop/apple-macbook-air-2020-mgn63saa".split(
                "https://www.thegioididong.com/laptop/"
            )[
                -1
            ]

        try:
            brand = driver.find_element(
                By.XPATH, "/html/body/section[1]/ul/li[2]/a"
            ).text.replace("Laptop", "").upper()
        except:
            brand = "null"
        try:
            price = driver.find_element(By.CSS_SELECTOR, "p.box-price-present").text
        except:
            price = " Not Sale"
        try:
            oldPrice = driver.find_element(By.CSS_SELECTOR, "p.box-price-old").text
        except:
            oldPrice = "null"
        listProps = driver.find_elements(By.CSS_SELECTOR, "div.parameter ul li")
        text = ""
        index = 0
        for listProp in listProps:
            label = listProp.find_element(By.CSS_SELECTOR, "p.lileft").text

            infos = listProp.find_elements(By.CSS_SELECTOR, "div.liright span")
            for info in infos:
                text += info.text
                text += " "
            if "CPU:" in label:
                cpu = remove_frequency(text)

            if "RAM:" in label:
                ram = text.replace("(Hãng công bố) ","")


            if "cứng:" in label:
                storage = text

            if "Màn hình:" in label:
                display = text

            if "Card màn hình:" in label:
                graphicsCard = text

            if "Hệ điều hành:" in label:
                os = text
                os=os.replace("+ Office Home & Student vĩnh viễn","")

            if "thước" in label:
                weightAndSize = text
                weight = weightAndSize.split("Nặng")[1].strip()
                size = weightAndSize.split("Nặng")[0].strip()

            if "ra" in label:
                mfg_year = text

            index += 1
            text = ""
        time.sleep(1)
        imageLink = driver.find_element(
            By.CSS_SELECTOR, 'div[class="owl-item active"] a img'
        ).get_attribute("src")
        if imageLink is None:
            imageLink = driver.find_element(
                By.CSS_SELECTOR, 'div[class="owl-item"] a img'
            ).get_dom_attribute("src")
        name=remove_cpu_and_suffix(name)
        # Thêm thông tin của laptop vào danh sách laptop_info
        laptop_info.append(
            [
                id,
                brand,
                name,
                price,
                oldPrice,
                link,
                imageLink,
                cpu,
                display,
                ram,
                storage,
                graphicsCard,
                os,
                weight,
                size,
                mfg_year,
            ]
        )
        print(id, name, imageLink)

driver.quit()


ten_file = "thegioididong.csv"
with open(ten_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(
        [
            "ID",
            "Brand",
            "Name",
            "Price",
            "Old Price",
            "Link",
            "ImageLink",
            "Display",
            "CPU",
            "RAM",
            "Storage",
            "Graphics Card",
            "OS",
            "Weight",
            "Size",
            "Manufacturing Year",
        ]
    )
    writer.writerows(laptop_info)
