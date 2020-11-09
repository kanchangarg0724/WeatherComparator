from selenium import webdriver
import time
webURL = "https://weather.com/"
chromePath = "C:\\Projects\\chromedriver.exe"


def get_temp_with_selenium(city,tunits):

    try:
        driver = webdriver.Chrome(executable_path=chromePath)
        driver.maximize_window()
        driver.get(webURL)

        if tunits == "metric":
            time.sleep(5)  # Wait till page loads completely
            driver.find_element_by_name("triangle-down").click()
            driver.find_element_by_xpath("//span[@class='UnitSelector--UnitSelectorButtonTextC--2X1ap']").click()

        time.sleep(5)  # Wait till page loads completely
        driver.find_element_by_id('LocationSearch_input').send_keys(city)
        time.sleep(5)  # Wait till control loads completely
        driver.find_element_by_id('LocationSearch_listbox-0').click()
        time.sleep(5)  # Wait till page loads completely
        temp = driver.find_element_by_class_name('CurrentConditions--tempValue--3KcTQ').text
        driver.close()

        return float(temp[:-1])

    except Exception as err:
        print("Error: %s" % err)


if __name__=="__main__":
    print(get_temp_with_selenium("Chandigarh","metric"))