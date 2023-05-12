import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException



# HOW TO RUN
# On one terminal, run: 
#   sudo java -jar ~/Downloads/selenium-server-4.9.0.jar standalone --config ./tests/config.toml
# On other:
#   cd "/Users/namanchaturvedi/Documents/Product onboarding/automate/test1/"
#   clear & python ./tests/test2.py 

# Define passwords
def login(request):
    login_deets = ["","",""]
    if request == "correct":
        login_deets =["<HIDDEN>","<HIDDEN>","right"]
    elif request == "incorrect":
        login_deets = ["bj20152@astra.xlri.ac.in","namanbrdgffghowserstack","wrong"]
    return login_deets


browsers_list = ["chrome","firefox","safari"]
login_list = ["correct","incorrect"]

for browser_i in browsers_list:
    
    for login_i in login_list:
        if browser_i == "chrome":
            driver = webdriver.Remote(
            command_executor='http://192.168.29.4:4444',
            desired_capabilities=webdriver.DesiredCapabilities.CHROME
            )
        elif browser_i == "firefox":
            driver = webdriver.Remote(
            command_executor='http://192.168.29.4:4444',
            desired_capabilities=webdriver.DesiredCapabilities.FIREFOX
            )
        elif browser_i == "safari": 
            driver = webdriver.Remote(
            command_executor='http://192.168.29.4:4444',
            desired_capabilities=webdriver.DesiredCapabilities.SAFARI
       )

        login_deets = login(login_i)

        test_email = login_deets[0]
        test_password = login_deets[1]

        get_url = driver.current_url

        driver.get('https://www.browserstack.com/users/sign_in')
        driver.fullscreen_window
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'user_email_login')))
        # Enter your login credentials and click the login button
        driver.find_element("id", "user_email_login").send_keys(test_email)
        # find password input field and insert password as well
        driver.find_element("id", "user_password").send_keys(test_password)
        # click login button
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'commit')))
        driver.execute_script("arguments[0].scrollIntoView();", element)
        element.click()

        print("\n*****************Test in browser: ",browser_i,"*****************")
        # Check if the login was successful by looking for the user avatar element
        try:
            WebDriverWait(driver, 20).until(EC.url_changes(('https://www.browserstack.com/users/sign_in')))
            live_dashboard_url = 'https://live.browserstack.com'
            if live_dashboard_url not in driver.current_url:
                driver.get(live_dashboard_url)
                WebDriverWait(driver, 5)
            assert live_dashboard_url in driver.current_url
            print('\nPass: Login for: ',login_i,' login\n')
            try:
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="platform-list-react"]/div/div[1]/div/div[4]/div[1]/div')))
                element.click()
                # print('Window click done')
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="platform-list-react"]/div/div[2]/div/div[2]/div[4]/div[1]/div[9]/div/div')))
                element.click()
                # print('edge click done')
    
                print('Pass: Dashboard for: ',login_i,' login\n')
                driver.quit()
            except:
                print('Fail: Dashboard for: ',login_i,' login\n')
                driver.quit()
        except AssertionError:
            print('\nFail: Login for: ',login_i,' login\n')
            driver.quit()
        except TimeoutException:
            print('\nFail: Login for: ',login_i,' login\n')
            driver.quit()
        except:
            # print('\nFail: Login: ', driver.name,"for cretentials:",login[2],"due to unknown reason\n")
            print('\nFail: Login (unkown reason) for: ',login_i,' login\n')
            driver.quit()