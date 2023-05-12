import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Observations - Safari gives errors. Permission issues. Product idea: BS extension for xpath copy
# HOW TO RUN
# cd "/Users/namanchaturvedi/Documents/Product onboarding/automate/test1/"
# clear & pytest -n 6 -s ./tests/test4.py

@pytest.fixture(params=["chrome", "firefox","safari"])
def browser(request):
    if request.param == "chrome":
        driver = webdriver.Chrome()
    elif request.param == "firefox":
        driver = webdriver.Firefox()
    elif request.param == "safari":
        driver = webdriver.Safari()
        # driver = webdriver.Safari(executable_path='/usr/bin/safaridriver')

    else:
        raise ValueError("Invalid browser: {}".format(request.param))
    
    yield driver
    
    driver.quit()

# Define passwords
@pytest.fixture(params=["correct", "incorrect"])
def login(request):
    login_deets = ["","",""]
    if request.param == "right":
        login_deets = ["<HIDDEN>","<HIDDEN>","right"]
    elif request.param == "wrong":
        login_deets = ["bj20152@astra.xlri.ac.in","namanbrdgffghowserstack","wrong"]
    return login_deets



def test_browserstack_login(browser,login):
    driver = browser
    test_email = login[0]
    test_password = login[1]

    driver.get('https://www.browserstack.com/users/sign_in')
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'user_email_login')))
    # Enter your login credentials and click the login button
    driver.find_element("id", "user_email_login").send_keys(test_email)
    # find password input field and insert password as well
    driver.find_element("id", "user_password").send_keys(test_password)
    # click login button
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'commit')))
    driver.execute_script("arguments[0].scrollIntoView();", element)
    element.click()

    # print("\n*****************Test: ",login[2]," login, in browser: ",driver.name,"*****************")
    # Check if the login was successful by looking for the user avatar element
    try:
        WebDriverWait(driver, 20)
        live_dashboard_url = 'https://live.browserstack.com'
        if live_dashboard_url not in driver.current_url:
            driver.get(live_dashboard_url)
            WebDriverWait(driver, 5)
        assert live_dashboard_url in driver.current_url
        print(driver.name,':\n\tPass: Login for: ',login[2],' login\n')
        print('\nPass: Login\n')
        try:
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="platform-list-react"]/div/div[1]/div/div[4]/div[1]/div')))
            element.click()
            # print('Window click done')
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="platform-list-react"]/div/div[2]/div/div[2]/div[4]/div[1]/div[7]/div/div')))
            element.click()
            # print('edge click done')
 
            print(driver.name,':\n\tPass: Dashboard for: ',login[2],' login\n')
            driver.quit()
        except:
            print(driver.name,':\n\tFail: Dashboard for: ',login[2],' login\n')
            driver.quit()
    except AssertionError:
        print(driver.name,':\n\tFail: Login for: ',login[2],' login\n')
    # except TimeoutError as terr:
    #     print('\nFail: Login: ', driver.name, 'for cretentials:',login[2],"\n")
    except:
        # print('\nFail: Login: ', driver.name,"for cretentials:",login[2],"due to unknown reason\n")
        print(driver.name,':\n\tFail: Login (unkown reason) for: ',login[2],' login\n')
        driver.quit()