import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

a = []
id = 0
for i in range(1, 6):
    url = "https://phongvu.vn/c/laptop?page=" + str(i)
    driver.get(url)
    laptopLink = driver.find_elements(By.CSS_SELECTOR, "div.css-13w7uog div a")
    for link in laptopLink:
        lplink = link.get_attribute("href")
        print(lplink)
        a.append(lplink)
laptop_info = []
driver.implicitly_wait(20)
for link in a:
    id += 1
    if id >0:
        driver.get(link)
        name = (
            driver.find_element(By.CSS_SELECTOR, "h1.css-4kh4rf")
            .text.split("(")[0]
            .replace("Laptop", "")
            .replace("Liên hệ đặt hàng", "")
            .replace("Máy tính xách tay/", "")
            .strip()
            .upper()
        )
        imageLink = driver.find_element(
            By.CSS_SELECTOR, "div.css-j4683g img"
        ).get_attribute("src")
        brand = name.split()[0]
        try:
            price = driver.find_element(
                By.CSS_SELECTOR,
                'div[class="att-product-detail-latest-price css-z55zyl"]',
            ).text
        except:
            price = "null"
        try:
            oldPrice = driver.find_element(
                By.CSS_SELECTOR,
                'div[class="att-product-detail-retail-price css-164smgo"]',
            ).text
        except:
            oldPrice = "null"
        cpu = driver.find_element(
            By.XPATH,
            "/html/body/div[2]/div/div/div/div/div[4]/div/div/div[2]/div[1]/div/div/div[1]/div[3]",
        ).text
        lines = cpu.split("\n")

        info_dict = {}
        for line in lines:
            print(line)
            if ":" in line:
                if len(line.split(":")) == 3:
                    keypin, value, valueSize = line.split(":")
                    pin, size = value.split(",")
                    info_dict[keypin] = pin
                    info_dict["- Khối lượng"] = valueSize
                else:
                    key, value = line.split(":")
                    key = key.strip()
                    value = value.strip()
                    info_dict[key] = value
            else:
                info_dict["- Pin"] = line.strip()
        if "- Khối lượng" not in info_dict:
            info_dict["- Khối lượng"] = "null"
        if "- CPU" in info_dict and "- Hệ điều hành" in info_dict :
            info_dict["- CPU"]=info_dict["- CPU"].replace('Intel Core', '').replace("AMD","")
            info_dict["- Khối lượng"]= info_dict["- Khối lượng"].replace("kg"," kg")
            laptop_info.append(
                [
                    id,
                    brand,
                    name,
                    price,
                    oldPrice,
                    link,
                    imageLink,
                    info_dict["- CPU"],
                    info_dict["- Màn hình"],
                    info_dict["- RAM"],
                    info_dict["- Đồ họa"],
                    info_dict["- Lưu trữ"],
                    info_dict["- Hệ điều hành"],
                    info_dict["- Pin"],
                    info_dict["- Khối lượng"],
                ]
            )
        print(id, name, imageLink)

driver.quit()


ten_file = "phongvu.csv"
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
            "CPU",
            "Display",
            "RAM",
            "Graphics Card",
            "Storage",
            "OS",
            "Battery",
            "Weight",
        ]
    )
    writer.writerows(laptop_info)
