import requests
import warnings
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore
from pystyle import Center, Colors, Colorate
import os
import time

warnings.filterwarnings("ignore", category=DeprecationWarning)

def save_settings(twitch_username, set_160p):
    with open('settings.txt', 'w') as file:
        file.write(f"Twitch Username: {twitch_username}\n")
        file.write(f"Set 160p: {set_160p}\n")

def load_settings():
    try:
        with open('settings.txt', 'r') as file:
            lines = file.readlines()
            if len(lines) >= 2:
                twitch_username = lines[0].split(': ')[1].strip()
                set_160p = lines[1].split(': ')[1].strip()
                return twitch_username, set_160p
    except:
        pass
    return None, None




def set_stream_quality(driver, quality):
    if quality == "yes":
        element_xpath = "//div[@data-a-target='player-overlay-click-handler']"
        quality_option_xpath = "//label[contains(., '160p')]"
        
        try:
            # Espera até que o elemento esteja presente na página
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, element_xpath))
            )

            # Continue com a mudança de qualidade do stream
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()

            settings_button = driver.find_element(By.XPATH, "//button[@aria-label='Settings']")
            settings_button.click()

            # Espera até que a opção de qualidade esteja clicável
            quality_option = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//div[text()='Quality']"))
            )
            quality_option.click()

            # Clicar diretamente na opção "160p"
            quality_element = driver.find_element(By.XPATH, quality_option_xpath)
            driver.execute_script("arguments[0].style.backgroundColor = 'yellow';", quality_element)  # Realça o elemento
            quality_element.click()
            driver.execute_script("arguments[0].style.backgroundColor = '';", quality_element)  # Remove a marcação após o clique
                
        except Exception as e:
            print("Erro ao definir a qualidade do stream:")
            print(e)

def main():
    
    twitch_username, set_160p = load_settings()

    os.system(f"title Twitch Viewer ")
    
    run_headless = input(Colorate.Vertical(Colors.green_to_blue, "Do you want to run the script in headless mode? (yes/no): ")).lower() == "yes"
    

    proxy_servers = ['https://www.blockaway.net', 'https://www.coxyproxy.com', 'https://www.croxyproxy.rocks', 'https://www.croxy.network', 'https://www.croxy.org', 'https://www.youtubeunblocked.live', 'https://www.croxyproxy.net']
    def selectRandom(proxy_servers):
        return random.choice(proxy_servers)

    proxy_url = selectRandom(proxy_servers)

    print(Colors.red, "Proxy servers are randomly selected every time")
    
    if twitch_username is None or set_160p is None:
        
        twitch_username = input(Colorate.Vertical(Colors.green_to_blue, "Enter your channel name (e.g Kichi779): "))
        set_160p = input(Colorate.Vertical(Colors.purple_to_red,"Do you want to set the stream quality to 160p? (yes/no): "))

        save_settings(twitch_username, set_160p)

    else:
        use_settings = input(Colorate.Vertical(Colors.green_to_blue, "Do you want to use your saved settings? (yes/no): "))
        if use_settings.lower() == "no":
            
            twitch_username = input(Colorate.Vertical(Colors.green_to_blue, "Enter your channel name (e.g Kichi779): "))
            set_160p = input(Colorate.Vertical(Colors.purple_to_red,"Do you want to set the stream quality to 160p? (yes/no): "))

            save_settings(twitch_username, set_160p)
        
    proxy_count = int(input(Colorate.Vertical(Colors.cyan_to_blue, "How many proxy sites do you want to open? (Viewer to send)")))


    os.system("cls")

    print('')
    print('')
    print(Colors.red, Center.XCenter("Viewers Send. Please don't hurry. If the viewers does not arrive, turn it off and on and do the same operations"))


    chrome_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    driver_path = 'chromedriver.exe'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument("--lang=en")
    if run_headless:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument('--disable-dev-shm-usage')

    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print("Erro ao criar o driver do Chrome:")
        print(e)
        return

    driver.get(proxy_url)
    
    counter = 0 

    for i in range(proxy_count):
        random_proxy_url = selectRandom(proxy_servers)  # Select a random proxy server for this tab
        driver.execute_script("window.open('" + random_proxy_url + "')")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(random_proxy_url)


        try:
            text_box = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, 'url'))
            )
            text_box.send_keys(f'www.twitch.tv/{twitch_username}')
            text_box.send_keys(Keys.RETURN)
            time.sleep(15)
            
            counter += 1  # Increment the counter for each driver created
            print(f"Virtual viewer {counter}/{proxy_count} spawned.")  # Print the counter and total count

        except Exception as e:
            print("Erro ao enviar os viewers:")
            print(e)
        
    set_stream_quality(driver, set_160p)

    input(Colorate.Vertical(Colors.red_to_blue, "Viewers have all been sent. You can press enter to withdraw the views and the program will close."))
    driver.quit()

if __name__ == '__main__':
    main()

