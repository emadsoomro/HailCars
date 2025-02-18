import time
from utils import Handywrapper
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
import psycopg2
from psycopg2 import sql
from datetime import datetime
import re
from selenium.webdriver.chrome.options import Options

class HailCars:

    def clean_text(self,text):
        return re.sub(r'[^a-zA-Z0-9 ]', '', text)

    # PW_Locations =["Karachi", "Lahore", "Islamabad", "Rawalpindi", "Peshawar", "Quetta","Abbottabad","Bahawalpur","Faisalabad","Gujranwala","Haripur", "Hyderabad","Jhelum", "Kashmir", "Larkana","Mian Wali", "Mirpur khas", "Multan","Murree", "Muzaffar Gargh", "Muzaffarabad", "Nawabshah","Rahim Yar Khan","Sadiqabad","Sahiwal","Sargodha","Sialkot","Sukkur","Taxila"]
    PW_Locations =["Karachi","Lahore", "Islamabad", "Hyderabad","Multan"]
    # PW_Locations =["Islamabad", "Hyderabad","Multan"]
    # Makes = ["Toyota", "Suzuki", "Honda", "Daihatsu", "Adam", "Audi", "BAIC", "BMW", "BYD", "Bentley",
    # "Buick", "Cadillac", "Changan", "Chery", "Chevrolet", "Chrysler", "DFSK", "Daehan", "Daewoo",
    # "Datsun", "Deepal", "Dodge", "FAW", "Fiat", "Ford", "GMC", "GUGO", "Geely", "Genesis",
    # "Golden Dragon", "Haval", "Hino", "Honri", "Hummer", "Hyundai", "Isuzu", "JAC", "JW Forland",
    # "Jaguar", "Jeep", "KIA", "Lamborghini", "Land Rover", "Lexus", "MG", "MINI", "Master",
    # "Mazda", "Mercedes Benz", "Mitsubishi", "Nissan", "ORA", "Opel", "Peugeot", "Porsche", "Power",
    # "Prince", "Proton", "Range Rover", "Renault", "Rinco", "Rolls Royce", "Sogo", "SsangYong",
    # "Subaru", "Tank", "Tesla", "United", "Volkswagen", "Volvo", "Willys", "ZOTYE"]

    def pakwheels(self):
        database_cred = "postgresql://saim:R2_RkmUt3xc59Gjzuhn33A@joking-egret-7111.8nk.cockroachlabs.cloud:26257/HailCars?sslmode=require"

        conn = psycopg2.connect(database_cred)
        cursor = conn.cursor()
        table_name = "pakwheels"
        self.create_table(conn, cursor, table_name)

        Locations=self.PW_Locations
        # Makes = self.Makes


        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        # chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        # chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resources
        # chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (sometimes needed)
        chrome_options.add_argument("--window-size=1920x1080")

        wd = webdriver.Chrome(options=chrome_options)
        hw = Handywrapper(wd)
        for location in Locations:
            wd.get("https://www.pakwheels.com/used-cars")
            hw.wait_explicitly(By.XPATH, "//button[.='NO THANKS']")
            hw.Click_element(By.XPATH, "//button[.='NO THANKS']")
            hw.wait_explicitly(By.XPATH,"//span[.='All Cities']//parent::a[@href='javascript:void(0)']")
            hw.Click_element(By.XPATH,"//span[.='All Cities']//parent::a[@href='javascript:void(0)']")
            serach_city = hw.find_element(By.XPATH,"//span[.='All Cities']/parent::a//following-sibling::div/div[@class='chzn-search']/input")

            serach_city.send_keys(location)
            hw.Click_element(By.XPATH, f"//li[.='{location}' and contains(@id,'Used')]")
            hw.Click_element(By.XPATH,"//button[.='Search']")
            time.sleep(1)
            loading = hw.is_element_present(By.XPATH,"//i[@class='ajax-search-loader search-loader-fixed' and not @style='display: none;']")
            while loading:
                loading = hw.is_element_present(By.XPATH,"//i[@class='ajax-search-loader search-loader-fixed' and not @style='display: none;']")
                time.sleep(1)

            hw.Click_element(By.XPATH,"//a[contains(.,'Make')]/parent::div/following-sibling::div/div/span[contains(.,'more choices')]")
            hw.wait_explicitly(By.XPATH, "//li//input[@name='checkbox']")
            Makes = hw.get_list_of_attributes(By.XPATH, "//li//input[@name='checkbox']")
            Makes = list(map(lambda x: x.strip(), Makes))

            for make in Makes:
                time.sleep(0.5)
                hw.Click_element(By.XPATH,"//a[contains(.,'Make')]/parent::div/following-sibling::div/div/span[contains(.,'more choices')]")
                hw.Click_element(By.XPATH,"//button[.='Clear']")
                time.sleep(0.5)
                hw.wait_explicitly(By.XPATH, "//button[.='NO THANKS']", timeout=1)
                hw.Click_element(By.XPATH, "//button[.='NO THANKS']")
                hw.Click_element(By.XPATH,f"//input[@value='{make.lower()}' and @name='checkbox']")

                hw.Click_element(By.XPATH,"//button[@value='submit' and .='Submit']")
                time.sleep(1)
                loading = hw.is_element_present(By.XPATH,"//i[@class='ajax-search-loader search-loader-fixed' and not @style='display: none;']")
                while loading:
                    loading = hw.is_element_present(By.XPATH,"//i[@class='ajax-search-loader search-loader-fixed' and not @style='display: none;']")
                    print(loading)
                    time.sleep(1)

                hw.Click_element(By.XPATH,"//a[contains(.,'Model')]/parent::div/following-sibling::div/div/span[contains(.,'more choices')]")
                hw.wait_explicitly(By.XPATH,"//li//input[@name='checkbox']")
                Models = hw.get_list_of_attributes(By.XPATH,"//li//input[@name='checkbox']")
                Models = list(map(lambda x:x.strip(), Models))
                print(Models)
                for model in Models:
                    hw.wait_explicitly(By.XPATH,"//a[contains(.,'Model')]/parent::div/following-sibling::div/div/span[contains(.,'more choices')]")
                    hw.scroll_to_element(By.XPATH,"//a[contains(.,'Model')]/parent::div/following-sibling::div/div/span[contains(.,'more choices')]")
                    hw.Click_element(By.XPATH,"//a[contains(.,'Model')]/parent::div/following-sibling::div/div/span[contains(.,'more choices')]")
                    hw.Click_element(By.XPATH, "//button[.='Clear']")
                    hw.Click_element(By.XPATH, f"//input[@value='{model.lower()}' and @name='checkbox']")
                    hw.Click_element(By.XPATH, "//button[@value='submit' and .='Submit']")
                    loading = hw.is_element_present(By.XPATH, "//i[@class='ajax-search-loader search-loader-fixed' and not @style='display: none;']")
                    while loading:
                        loading = hw.is_element_present(By.XPATH,"//i[@class='ajax-search-loader search-loader-fixed' and not @style='display: none;']")
                        time.sleep(1)

                    time.sleep(1.5)

                    html_content = wd.page_source
                    soup = BeautifulSoup(html_content, 'html.parser')

                    script_tags = soup.find_all('script', type='application/ld+json')
                    script_tags =script_tags[2:]
                    parsed_data = []
                    for idx, script_tag in enumerate(script_tags, start=1):
                        item = {}
                        try:
                            item = json.loads(script_tag.string)

                        except json.JSONDecodeError:
                            print(f"Error decoding JSON in script tag {idx}")
                        URL =  hw.get_value_by_key("url", hw.get_value_by_key("offers", item))
                        Url = URL.replace("https://www.pakwheels.com", "")
                        hw.wait_explicitly(By.XPATH,f"//a[@href='{Url}']/parent::div/parent::div/parent::div/following-sibling::div[1]//ul[1]/li")
                        Location = hw.find_element_text(By.XPATH,f"//a[@href='{Url}']/parent::div/parent::div/parent::div/following-sibling::div[1]//ul[1]/li")

                        vehicle_details = {
                            "Brand": hw.get_value_by_key("name",hw.get_value_by_key("brand",item)),
                            "Description": hw.get_value_by_key("description",item),
                            "Condition": hw.get_value_by_key("itemCondition",item),
                            "Model Year": hw.get_value_by_key("modelDate",item),
                            "Manufacturer": hw.get_value_by_key("manufacturer",item),
                            "Fuel Type": hw.get_value_by_key("fuelType",item),
                            "Transmission": hw.get_value_by_key("vehicleTransmission",item),
                            "Engine": hw.get_value_by_key("engineDisplacement",hw.get_value_by_key("vehicleEngine",item)),
                            "Mileage": hw.get_value_by_key("mileageFromOdometer",item),
                            "Price": hw.get_value_by_key("price",hw.get_value_by_key("offers", item)),
                            "Currency": hw.get_value_by_key("priceCurrency",hw.get_value_by_key("offers", item)),
                            "URL": hw.get_value_by_key("url",hw.get_value_by_key("offers",item)),
                            "Image": hw.get_value_by_key("image",item),
                            "City": Location.strip(),
                            "Model": model.capitalize()
                        }

                        if vehicle_details["Brand"] != "" and vehicle_details["Description"] != "" and vehicle_details["Model"] != "" and vehicle_details["Image"] != "" and vehicle_details["City"] !="":
                            parsed_data.append(vehicle_details)

                            data_to_insert = (
                                str(vehicle_details['Brand']), str(vehicle_details['Description']), str(vehicle_details['Condition']),
                                str(vehicle_details['Model Year']), str(vehicle_details['Manufacturer']), str(vehicle_details['Fuel Type']),
                                str(vehicle_details['Transmission']), str(vehicle_details['Engine']), vehicle_details['Mileage'], vehicle_details['Price'],
                                str(vehicle_details['Currency']), str(vehicle_details['URL']), vehicle_details['Image'], vehicle_details['City'], vehicle_details['Model'],
                            datetime.now().isoformat())
                            try:
                                self.insert_data(conn, cursor,table_name, data_to_insert)
                            except Exception as e:
                                print(f"error: {e}")

                hw.wait_explicitly(By.XPATH,"//a[contains(.,'Model')]/parent::div/following-sibling::div/div/span[contains(.,'more choices')]")
                hw.scroll_to_element(By.XPATH, "//a[contains(.,'Model')]/parent::div/following-sibling::div/div/span[contains(.,'more choices')]")
                hw.Click_element(By.XPATH,"//a[contains(.,'Model')]/parent::div/following-sibling::div/div/span[contains(.,'more choices')]")
                hw.Click_element(By.XPATH, "//button[.='Clear']")
                hw.Click_element(By.XPATH, "//button[@value='submit' and .='Submit']")

                hw.wait_explicitly(By.XPATH,"//a[contains(.,'Make')]/parent::div/following-sibling::div/div/span[contains(.,'more choices')]")
                hw.scroll_to_element(By.XPATH, "//a[contains(.,'Make')]/parent::div/following-sibling::div/div/span[contains(.,'more choices')]")
                hw.Click_element(By.XPATH,"//a[contains(.,'Make')]/parent::div/following-sibling::div/div/span[contains(.,'more choices')]")
                hw.Click_element(By.XPATH, "//button[.='Clear']")
                hw.Click_element(By.XPATH, "//button[@value='submit' and .='Submit']")


    def olx(self):
        database_cred = "postgresql://saim:R2_RkmUt3xc59Gjzuhn33A@joking-egret-7111.8nk.cockroachlabs.cloud:26257/HailCars?sslmode=require"

        conn = psycopg2.connect(database_cred)
        cursor = conn.cursor()
        table_name = "olx"
        self.create_table(conn, cursor, table_name)
        Locations = self.PW_Locations
        makes = ["Suzuki", "Toyota", "Honda", "Daihatsu", "Nissan", "Mitsubishi", "KIA", "Changan", "Hyundai", "Mazda",
                  "FAW", "MG", "Prince", "Mercedes", "Chevrolet", "Isuzu", "Subaru", "Proton", "DFSK"]

        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resources
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (sometimes needed)
        chrome_options.add_argument("--window-size=1920x1080")

        wd = webdriver.Chrome(options=chrome_options)

        hw = Handywrapper(wd)
        for location in Locations:
            wd.get("https://www.olx.com.pk/cars_c84")
            hw.wait_explicitly(By.XPATH, f"(//span[contains(.,'{location}')])[1]")
            hw.Click_element(By.XPATH, f"(//span[contains(.,'{location}')])[1]")
            time.sleep(0.5)
            hw.Click_element(By.XPATH,"//span[contains(.,'Used')]/parent::label/preceding-sibling::input[@type='checkbox']")
            run =1
            for make in makes:
                time.sleep(0.5)
                if run ==1:
                    hw.Click_element(By.XPATH,f"//span[.='{make}']")
                    time.sleep(1)
                parsed_data = []
                model_el = hw.find_elements(By.XPATH,"//div[.='Brand and Model']/following-sibling::div//label/preceding-sibling::input[@type='checkbox']")
                for model_ind in range(len(model_el)):
                    run +=1
                    model_ind = model_ind + 1
                    hw.Click_element(By.XPATH, f"//span[.='{make}']")
                    time.sleep(1)
                    model = hw.find_element(By.XPATH,f"(//div[.='Brand and Model']/following-sibling::div//label/preceding-sibling::input[@type='checkbox'])[{model_ind}]")
                    hw.Click_element(element=model)
                    time.sleep(0.5)
                    model_text = hw.find_element_text(By_type=By.XPATH, locator=f"(//div[.='Brand and Model']/following-sibling::div//label/span)[{model_ind}]")
                    time.sleep(0.5)
                    items = hw.find_elements(By.XPATH, "//li[@aria-label='Listing']/article")
                    for item_ind in range(len(items)):
                        time.sleep(0.1)
                        item_ind = item_ind + 1
                        try:
                            # wd.execute_script(
                            #     "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", hw.find_element(By.XPATH,f"(//li[@aria-label='Listing']/article)[{item_ind}]/div//picture/source"))
                            hw.find_element(By.XPATH,f"(//li[@aria-label='Listing']/article)[{item_ind}]/div//picture/source")
                        except:
                            pass
                        Description = hw.get_attribute(By.XPATH, f"(//li[@aria-label='Listing']/article)[{item_ind}]/div/div/a","title")
                        Url = hw.get_attribute(By.XPATH, f"(//li[@aria-label='Listing']/article)[{item_ind}]/div/div/a","href")
                        Image = hw.get_attribute(By.XPATH, f"(//li[@aria-label='Listing']/article)[{item_ind}]/div//picture/source", "srcset")
                        Price = hw.find_element_text(By.XPATH,f"(//li[@aria-label='Listing']/article)[{item_ind}]/div/div/div[@aria-label='Price']/span")
                        Location = hw.find_element_text(By.XPATH,f"(//li[@aria-label='Listing']/article)[{item_ind}]/div/div/div/span[@aria-label='Location']")
                        Mileage = hw.find_element_text(By.XPATH,f"(//li[@aria-label='Listing']/article)[{item_ind}]/div/div//span[@aria-label='Mileage']/span")
                        ModelYear = hw.find_element_text(By.XPATH,f"(//li[@aria-label='Listing']/article)[{item_ind}]/div/div//span[@aria-label='Year']/span")
                        FuelType = hw.find_element_text(By.XPATH,f"(//li[@aria-label='Listing']/article)[{item_ind}]/div/div//span[@aria-label='FuelType']/span")
                        Currency = Price.split(' ')[0]
                        Price = Price.split(' ')[-1]
                        model = "".join(model_text.split("(")[:-1]).strip()

                        Location_ = Location.split(',')[-1]
                        Location_ = Location_.strip()
                        Location_ = self.clean_text(Location_)
                        if Location_.lower() == "pakistan":
                            try:
                                Location_ = Location.split(',')[-2]
                                Location_ = Location_.strip()
                                Location_ = self.clean_text(Location_)
                                if Location_.lower() == "islamabad capital territory":
                                    Location_ = "Islamabad"
                            except:
                                pass

                        vehicle_details = {
                            "Brand": make.strip(),
                            "Description": Description.strip(),
                            "Condition": "used",
                            "Model Year": ModelYear.strip(),
                            "Manufacturer": make.strip(),
                            "Fuel Type": FuelType.strip(),
                            "Transmission": "",
                            "Engine": "",
                            "Mileage": Mileage.strip(),
                            "Price": Price.strip(),
                            "Currency": Currency.strip(),
                            "URL": Url.strip(),
                            "Image": Image.strip(),
                            "City": Location_.strip(),
                            "Model": model.strip()
                        }

                        if make.lower() not in Url and make.lower() not in Description.lower():
                            continue

                        if vehicle_details["Brand"] != "" and vehicle_details["Description"] != "" and vehicle_details["Model"] != "" and vehicle_details["Image"] != "" and vehicle_details[
                            "City"] != "":
                            parsed_data.append(vehicle_details)

                            data_to_insert = (
                                str(vehicle_details['Brand']), str(vehicle_details['Description']),
                                str(vehicle_details['Condition']),
                                str(vehicle_details['Model Year']), str(vehicle_details['Manufacturer']),
                                str(vehicle_details['Fuel Type']),
                                str(vehicle_details['Transmission']), str(vehicle_details['Engine']),
                                vehicle_details['Mileage'], vehicle_details['Price'],
                                str(vehicle_details['Currency']), str(vehicle_details['URL']), vehicle_details['Image'], vehicle_details['City'], vehicle_details['Model'],
                            datetime.now().isoformat())
                            try:
                                self.insert_data(conn, cursor, table_name, data_to_insert)
                            except Exception as e:
                                print(f"error: {e}")

                    time.sleep(0.5)
                    try:
                        # wd.execute_script(
                        #     "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                        # hw.find_element(By.XPATH, "//a[.='Clear']"))
                        hw.find_element(By.XPATH, "//a[.='Clear']")
                    except:
                        pass
                    hw.Click_element(By.XPATH, "//a[.='Clear']")
                    time.sleep(1)

    def gari(self):
        database_cred = "postgresql://saim:R2_RkmUt3xc59Gjzuhn33A@joking-egret-7111.8nk.cockroachlabs.cloud:26257/HailCars?sslmode=require"

        conn = psycopg2.connect(database_cred)
        cursor = conn.cursor()
        table_name = "gari"
        self.create_table(conn, cursor, table_name)
        Locations = self.PW_Locations
        makes = ["Suzuki", "Toyota", "Honda", "Daihatsu", "Nissan", "Mitsubishi", "Hyundai", "Mercedes Benz", "Kia", "Mazda", "BMW", "Audi", "Faw", "Chevrolet", "Subaru", "Daewoo", "Lexus", "United", "Jeep", "Adam", "Prince", "Changan", "Land Rover", "Range Rover", "Chery", "Alfa Romeo", "Porsche", "Volkswagen", "Ford", "SsangYong", "Isuzu", "Fiat", "Datsun", "Bentley", "Classic Cars", "Mini", "Cadillac", "Buick", "Sogo", "Others", "Master", "Roma", "Austin", "DFSK", "Willys", "Geely", "JAC", "Dodge", "Jaguar", "Hummer", "Hino", "Seat", "Acura", "Dongfeng", "JW Forland", "Peugeot", "Morris", "Proton", "Vauxhall", "Sokon", "Saab", "Oldsmobile", "Chrysler", "Golden Dragon", "Scion", "JMC"]

        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resources
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (sometimes needed)
        chrome_options.add_argument("--window-size=1920x1080")

        wd = webdriver.Chrome(options=chrome_options)
        hw = Handywrapper(wd)
        for location in Locations:
            wd.get("https://www.gari.pk/used-cars-search/")
            hw.wait_explicitly(By.XPATH, f"//div[@id='cities']/following-sibling::div[contains(.,'More Options')]")
            hw.Click_element(By.XPATH, f"//div[@id='cities']/following-sibling::div[contains(.,'More Options')]")
            hw.wait_explicitly(By.XPATH, f"//span[.='Clear']")
            hw.Click_element(By.XPATH, f"//span[.='Clear']")
            hw.wait_explicitly(By.XPATH, f"//div[contains(@class,'alert')]//a[.='{location}']/preceding-sibling::input")
            hw.Click_element(By.XPATH, f"//div[contains(@class,'alert')]//a[.='{location}']/preceding-sibling::input")
            hw.Click_element(By.XPATH, f"//button[.='OK']")
            for make in makes:
                hw.Click_element(By.XPATH, f"//button[.='OK']")
                hw.Click_element(By.XPATH,f"//div[@id='inner-makes-cont']/following-sibling::div[contains(.,'More Options')]")
                hw.Click_element(By.XPATH, f"//button[.='Later']")
                hw.wait_explicitly(By.XPATH, f"//span[.='Clear']")
                hw.Click_element(By.XPATH, f"//span[.='Clear']")
                hw.wait_explicitly(By.XPATH,f"//div[contains(@class,'alert')]//a[.='{make}']/preceding-sibling::input")
                hw.Click_element(By.XPATH,f"//div[contains(@class,'alert')]//a[.='{make}']/preceding-sibling::input")
                hw.Click_element(By.XPATH, f"//button[.='OK']")
                time.sleep(1)
                hw.Click_element(By.XPATH,f"//div[@id='inner-models-cont']/following-sibling::div[contains(.,'More Options')]")
                models = hw.find_elements_list_of_text(By.XPATH, "//div[@id='models_popUp']/div/label/a")
                parsed_data = []
                for model in models:
                    # hw.wait_explicitly(By.XPATH,f"//div[@id='models']/following-sibling::div[@class='more_options']")
                    # hw.Click_element(By.XPATH,f"//div[@id='models']/following-sibling::div[@class='more_options']")
                    # hw.wait_explicitly(By.XPATH, f"//span[.='Clear']")
                    # hw.Click_element(By.XPATH, f"//span[.='Clear']")
                    hw.wait_explicitly(By.XPATH, f"//div[contains(@class,'alert')]//input[@value='{model}']")
                    time.sleep(0.5)
                    hw.Click_element(By.XPATH, f"//div[contains(@class,'alert')]//input[@value='{model}']")
                    hw.Click_element(By.XPATH, f"//button[.='OK']")
                    hw.wait_explicitly(By.XPATH,f"//div[@id='cat-contents']")
                    items = hw.find_elements(By.XPATH,f"//div[@id='cat-contents']")
                    time.sleep(0.5)
                    for item_ind in range(len(items)):
                        item_ind = item_ind + 1
                        try:
                            # wd.execute_script(
                            #     "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", hw.find_element(By.XPATH,f"//div[@id='cat-contents'][{item_ind}]"))
                            hw.find_element(By.XPATH,f"//div[@id='cat-contents'][{item_ind}]")
                        except:
                            pass
                        hw.wait_explicitly(By.XPATH, f"//div[contains(@id,'popup')]/button[@class='close-btn']", 3)
                        hw.Click_element(By.XPATH, f"//div[contains(@id,'popup')]/button[@class='close-btn']")
                        hw.wait_explicitly(By.XPATH, f"(//div[@id='price-cat'])[{item_ind}]/div")
                        time.sleep(1)
                        item_details = hw.find_elements_list_of_text(By.XPATH, f"(//div[@id='price-cat'])[{item_ind}]/div")
                        if len(item_details) > 0:
                            Description = hw.find_element_text(By.XPATH, f"(//div[@id='ad-title'])[{item_ind}]//span")
                            Url = hw.get_attribute(By.XPATH, f"(//div[@id='image-cat'][1]//a)[{item_ind}]","href")
                            Image = hw.get_attribute(By.XPATH, f"(//div[@id='image-cat'][1]//a/img)[{item_ind}]", "src")
                            Mileage = item_details[2]
                            ModelYear = item_details[0]
                            FuelType = item_details[4]

                            try:
                                Currency = item_details[3].split(' ')[0]
                                Price = item_details[3].split(' ')[1]
                                Price = int(float(Price) * 100000)
                            except:
                                Currency = "Rs."
                                Price = item_details[3]
                            # model = model

                            vehicle_details = {
                                "Brand": make.strip(),
                                "Description": Description.strip(),
                                "Condition": "used",
                                "Model Year": ModelYear.strip(),
                                "Manufacturer": make.strip(),
                                "Fuel Type": FuelType.strip(),
                                "Transmission": item_details[6].strip(),
                                "Engine": item_details[5].strip(),
                                "Mileage": Mileage.strip(),
                                "Price": Price.strip(),
                                "Currency": Currency.strip(),
                                "URL": Url.strip(),
                                "Image": Image.strip(),
                                "City": item_details[1].strip(),
                                "Model": model.strip()
                            }

                            if make.lower() not in Url and make.lower() not in Description.lower():
                                continue

                            if vehicle_details["Brand"] != "" and vehicle_details["Description"] != "" and vehicle_details["Model"] != "" and vehicle_details["Image"] != "" and vehicle_details[
                                "City"] != "":
                                parsed_data.append(vehicle_details)

                                data_to_insert = (
                                    str(vehicle_details['Brand']), str(vehicle_details['Description']),
                                    str(vehicle_details['Condition']),
                                    str(vehicle_details['Model Year']), str(vehicle_details['Manufacturer']),
                                    str(vehicle_details['Fuel Type']),
                                    str(vehicle_details['Transmission']), str(vehicle_details['Engine']),
                                    vehicle_details['Mileage'], vehicle_details['Price'],
                                    str(vehicle_details['Currency']), str(vehicle_details['URL']), vehicle_details['Image'], vehicle_details['City'], vehicle_details['Model'],
                                    datetime.now().isoformat())
                                try:
                                    self.insert_data(conn, cursor, table_name, data_to_insert)
                                except Exception as e:
                                    print(f"error: {e}")

                    time.sleep(0.5)
                    try:
                        hw.wait_explicitly(By.XPATH,
                                           f"//div[@id='models']/following-sibling::div[@class='more_options']")
                        hw.Click_element(By.XPATH, f"//div[@id='models']/following-sibling::div[@class='more_options']")
                        # wd.execute_script(
                        #     "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                        #     hw.find_element(By.XPATH, "//div[@id='models']/following-sibling::div[@class='more_options']"))
                    except:
                        pass
                    hw.wait_explicitly(By.XPATH, f"//span[.='Clear']")
                    hw.Click_element(By.XPATH, f"//span[.='Clear']")


    def create_table(self,conn, cursor, table_name):
        table_name = sql.Identifier(table_name)
        create_table_query = sql.SQL('''CREATE TABLE IF NOT EXISTS {} (
            id SERIAL PRIMARY KEY,
            brand VARCHAR(255),
            description TEXT,
            condition VARCHAR(50),
            model_year VARCHAR(50),
            manufacturer VARCHAR(255),
            fuel_type VARCHAR(50),
            transmission VARCHAR(50),
            engine VARCHAR(50),
            mileage VARCHAR(50),
            price VARCHAR(50),
            currency VARCHAR(25),
            url TEXT UNIQUE,
            image TEXT,
            city VARCHAR(50),
            model VARCHAR(255),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );''').format(table_name)

        cursor.execute(create_table_query)
        conn.commit()

    def insert_data(self, conn, cursor, table_name, data):
        table_name = sql.Identifier(table_name)
        insert_query = sql.SQL("""
                INSERT INTO {} (
                    brand,
                    description,
                    condition,
                    model_year,
                    manufacturer,
                    fuel_type,
                    transmission,
                    engine,
                    mileage,
                    price,
                    currency,
                    url,
                    image,
                    city,
                    model,
                    timestamp
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (url) DO UPDATE
                SET 
                    brand = EXCLUDED.brand,
                    description = EXCLUDED.description,
                    condition = EXCLUDED.condition,
                    model_year = EXCLUDED.model_year,
                    manufacturer = EXCLUDED.manufacturer,
                    fuel_type = EXCLUDED.fuel_type,
                    transmission = EXCLUDED.transmission,
                    engine = EXCLUDED.engine,
                    mileage = EXCLUDED.mileage,
                    price = EXCLUDED.price,
                    currency = EXCLUDED.currency,
                    image = EXCLUDED.image,
                    city = EXCLUDED.city,
                    model = EXCLUDED.model,
                    timestamp = EXCLUDED.timestamp;
            """).format(table_name)

        cursor.execute(insert_query, data)
        conn.commit()
        print(f"record inserted {data}")
HailCars = HailCars()
HailCars.pakwheels()

