import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException



# HOW TO RUN
# Observation: rate limited even on BS browsers. Also, the driver thing took some time to understand
# cd "/Users/namanchaturvedi/Documents/Product onboarding/automate/test1/"
# clear & python ./tests/test1.py  

# Define passwords
def login(request):
    login_deets = ["","",""]
    if request == "correct":
        login_deets = ["<HIDDEN>","<HIDDEN>","right"]
    elif request == "incorrect":
        login_deets = ["bj20152@astra.xlri.ac.in","namanbrdgffghowserstack","wrong"]
    return login_deets


browsers_list = ["safari"]
login_list = ["correct","incorrect"]

for browser_i in browsers_list:
    
    for login_i in login_list:
        if browser_i == "chrome":
            driver = webdriver.Chrome()
        elif browser_i == "firefox":
            driver = webdriver.Firefox()
        elif browser_i == "safari": 
            driver = webdriver.Safari()

        login_deets = login(login_i)

        test_email = login_deets[0]
        test_password = login_deets[1]

        get_url = driver.current_url

        driver.get('https://www.browserstack.com/users/sign_in')
        driver.fullscreen_window()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'user_email_login')))
        # Enter your login credentials and click the login button
        driver.find_element("id", "user_email_login").send_keys(test_email)
        # find password input field and insert password as well
        driver.find_element("id", "user_password").send_keys(test_password)
        # click login button
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'commit')))
        driver.execute_script("arguments[0].scrollIntoView();", element)
        element.click()
        # Check if the login was successful by looking for the user avatar element
        try:
            WebDriverWait(driver, 20).until(EC.url_changes(('https://www.browserstack.com/users/sign_in')))
            live_dashboard_url = 'https://live.browserstack.com'
            if live_dashboard_url not in driver.current_url:
                driver.get(live_dashboard_url)
                WebDriverWait(driver, 5)
                # print("live dashboard URL entered")

            WebDriverWait(driver, 10)
            assert live_dashboard_url in driver.current_url

            # print("assertion test done")

            print(browser_i,':\n\tPass: Login for: ',login_i,' login\n')
            try:
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="platform-list-react"]/div/div[1]/div/div[4]/div[1]/div')))
                element.click()
                # print('Window click done')
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="platform-list-react"]/div/div[2]/div/div[2]/div[4]/div[1]/div[9]/div/div')))
                element.click()
                # print('edge click done')
    
                print(browser_i,':\n\tPass: Dashboard for: ',login_i,' login\n')
                driver.quit()
            except:
                print(browser_i,':\n\tFail: Dashboard for: ',login_i,' login\n')
                driver.quit()
        except AssertionError:
            print(browser_i,':\n\tFail: Login for: ',login_i,' login\n')
            driver.quit()
        # except TimeoutError as terr:
        #     print('\nFail: Login: ', driver.name, 'for cretentials:',login[2],"\n")
        except TimeoutException:
            print(browser_i,':\n\tFail: Login for: ',login_i,' login\n')
            driver.quit()
        except:
            # print('\nFail: Login: ', driver.name,"for cretentials:",login[2],"due to unknown reason\n")
            print(browser_i,':\n\tFail: Login (unkown reason) for: ',login_i,' login\n')
            driver.quit()