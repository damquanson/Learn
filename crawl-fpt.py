import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import re

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def remove_cpu_and_suffix(string):
    pattern = r"\s+(i3|i5|i7|i9|R3|R5|R7|R9).*$"
    result = re.sub(pattern, "", string)
    return result.strip()

a = []
id = 0

driver.get("https://fptshop.com.vn/may-tinh-xach-tay?sort=ban-chay-nhat&trang=15")
laptop_card = driver.find_elements(
    By.CSS_SELECTOR, 'div[class="cdt-product prd-lap "]'
)

for laptop in laptop_card:
    
    laptopLink = laptop.find_element(
        By.CSS_SELECTOR, "div.cdt-product__img a"
    ).get_attribute("href")
    print(laptopLink)
    a.append(laptopLink)

# Khởi tạo danh sách để lưu thông tin laptop
laptop_info = []
driver.implicitly_wait(20)
for link in a:
    id += 1
    if id >0:
        driver.get(link)

        try:
            name = (
                driver.find_element(
                    By.CSS_SELECTOR,
                    "h1.st-name",
                )
                .text.split("/")[0]
                .replace("Laptop", "")
                .strip()
                .upper()
            )

        except:
            name = link.split("https://fptshop.com.vn/may-tinh-xach-tay/")[-1]
        print(id, name)
        try:
            price = driver.find_element(
                By.CSS_SELECTOR, 'div[class="st-price-main"]'
            ).text
            oldPrice = driver.find_element(
                By.CSS_SELECTOR, 'div[class="st-price-sub"] strike'
            ).text
        except:
            price = oldPrice = "null"

        print(price, oldPrice)
        try:
            brand = driver.find_element(
                By.CSS_SELECTOR, 'li[class="breadcrumb-item  active"] a'
            ).text.upper().replace('APPLE (MACBOOK)', 'MACBOOK')
        except:
            brand = "null"

        try:
            imageLink = driver.find_element(
                By.CSS_SELECTOR, 'div[class="swiper-slide swiper-slide-active"] img'
            ).get_attribute("src")
            display = driver.find_element(
                By.XPATH,
                '//*[@id="root"]/main/div/div[2]/div/div[1]/div[2]/div[1]/div/table/tbody/tr[1]/td[2]',
            ).text

            cpu = driver.find_element(
                By.XPATH,
                '//*[@id="root"]/main/div/div[2]/div/div[1]/div[2]/div[1]/div/table/tbody/tr[2]/td[2]',
            ).text.strip('"').replace("AMD,","").replace("Core ","").replace("Intel,","")
            ram = driver.find_element(
                By.XPATH,
                '//*[@id="root"]/main/div/div[2]/div/div[1]/div[2]/div[1]/div/table/tbody/tr[3]/td[2]',
            ).text.strip('"')
            storage = driver.find_element(
                By.XPATH,
                '//*[@id="root"]/main/div/div[2]/div/div[1]/div[2]/div[1]/div/table/tbody/tr[4]/td[2]',
            ).text.strip('"')
            graphicsCard = (
                driver.find_element(
                    By.XPATH,
                    '//*[@id="root"]/main/div/div[2]/div/div[1]/div[2]/div[1]/div/table/tbody/tr[5]/td[2]',
                )
                .text.strip('"')
                .replace(";", ",")
            )
            os = driver.find_element(
                By.XPATH,
                '//*[@id="root"]/main/div/div[2]/div/div[1]/div[2]/div[1]/div/table/tbody/tr[6]/td[2]',
            ).text.strip('"')
            weightLaptop = (
                driver.find_element(
                    By.XPATH,
                    '//*[@id="root"]/main/div/div[2]/div/div[1]/div[2]/div[1]/div/table/tbody/tr[7]/td[2]',
                )
                .text.strip('"')
                .replace(";", ",")
            )
            size = driver.find_element(
                By.XPATH,
                '//*[@id="root"]/main/div/div[2]/div/div[1]/div[2]/div[1]/div/table/tbody/tr[8]/td[2]',
            ).text.replace(";", ",")
            name = (
                driver.find_element(
                    By.CSS_SELECTOR,
                    "h1.st-name",
                )
                .text.split("/")[0]
                .replace("Laptop", "")
                .strip()
            )
            try:
                mfg_year = driver.find_element(
                    By.XPATH,
                    '//*[@id="root"]/main/div/div[2]/div/div[1]/div[2]/div[1]/div/table/tbody/tr[10]/td[2]',
                ).text
            except:
                mfg_year = "null"
            if "Windows" in graphicsCard.split():
                size = weightLaptop
                weightLaptop = os
                os = graphicsCard
                graphicsCard = "None"
                print(graphicsCard)
        except:
            display = (
                cpu
            ) = (
                link
            ) = (
                imageLink
            ) = (
                ram
            ) = storage = graphicsCard = os = weightLaptop = size = mfg_year = "null"
        name=remove_cpu_and_suffix(name)
        # hông tin của laptop vào danh sách laptop_info
        laptop_info.append(
            [
                id,
                brand,
                name,
                cpu,
                weightLaptop,
                price,
                oldPrice,
                link,
                imageLink,
                display,
                
                ram,
                storage,
                graphicsCard,
                os,
                
                size,
                mfg_year,
            ]
        )

driver.quit()

# Ghi thông tin từ danh sách laptop_info vào tệp CSV
ten_file = "fptshop.csv"
with open(ten_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(
        [
            "ID",
            "Brand",
            "Name",
            "CPU",
            "Weight",
            "Price",
            "OldPrice",
            "Link",
            "ImageLink",
            "Display",
            
            "RAM",
            "Storage",
            "Graphics Card",
            "OS",
            
            "Size",
            "Manufacturing Year",
        ]
    )
    writer.writerows(laptop_info)
