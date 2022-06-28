import textwrap
from urllib.request import urlopen
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


driverOptions = webdriver.ChromeOptions()
driverOptions.add_argument = {'user-data-dir':'/Users/Application/Chrome/Default'}
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=driverOptions)
wait = ui.WebDriverWait(driver, 240)
wait_frame = ui.WebDriverWait(driver, 25)
wait_button = ui.WebDriverWait(driver, 15)



def connect_page(url : str) -> None:
    driver.get(url)
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH,'//ul//button//*[name()="svg" and @class="app-svg icons-chat"]')))
        chat_button = driver.find_element_by_xpath('//ul//button//*[name()="svg" and @class="app-svg icons-chat"]')
        time.sleep(2)
        me = driver.find_element_by_tag_name("profile-picture")
        me_name = me.find_element_by_tag_name("img").get_attribute("alt").replace("Profile picture of",'').replace(".",'').strip()
        print(f"Logged in as {me_name}")
        chat_button.click()
        time.sleep(7)
        not_all = ["*",".", '"', "/", "'\'" ,"[", "]",":", ";","|", ","]
        wait_button.until(EC.presence_of_element_located((By.XPATH,'//ul[@aria-label="Chat list"]')))
    
        buttons = driver.find_elements_by_xpath('//ul[@aria-label="Chat list"]//*[@role="treeitem"]//span[starts-with(@class,"cle-title")]')

        for button in buttons:
            action = ActionChains(driver)
            hover = action.move_to_element(button)
            hover.perform()
            time.sleep(2)
            button.click()
            print("Working ...")
            time.sleep(7)
            
            try:
                wait_button.until(EC.presence_of_element_located((By.XPATH,'//div/h2')))
                name = driver.find_element_by_xpath('//div/h2').text

            except:
                wait_button.until(EC.presence_of_element_located((By.XPATH,'//span[@id="chat-header-title"]')))
                name = driver.find_element_by_xpath('//span[@id="chat-header-title"]').text
            
            def pull_ul():
                chat_frame = driver.find_element_by_xpath("//iframe[starts-with(@id, 'experience-container-')]")
                driver.switch_to.frame(chat_frame)
                wait_button.until(EC.presence_of_element_located((By.XPATH,'//ul[@aria-label="Chat content"]')))
                the_ul =driver.find_element(By.XPATH,'//ul[@aria-label="Chat content"]')
                new_lis =the_ul.find_elements(By.TAG_NAME,'li')
                return new_lis

            lis = pull_ul()
            for i in not_all:
                    if i in name:
                        name = name.replace(i, "")
            print(f"Archiving Chat with {name} ...\n")

            with open(f'{name} log.txt', 'w', encoding="utf-8") as f:
                f.write("CHAT: "+ name + '\n'+"-----------------------------------------------------------CHAT--------------------------------------------------------------------"'\n')
                def pull_msg(lis: list) -> None:

                    for i in lis:
                        
                        msg_write=[]
                        try:
                            
                            
                            author = i.find_element(By.XPATH,'.//div[@class="ui-chat__messageheader"]/span').text
                            txt=i.find_element(By.XPATH,'.//div[@class="ui-chat__messageheader"]/time').get_attribute('title')
                            f.write('\n')
                            msg_write.append(f"({author})"+ txt + '\n')

                            try:
                                msg_attach = i.find_element(By.XPATH,'.//*[starts-with(@id, "attachments-")]')
                                msg_text_plus = msg_attach.get_attribute('aria-label')
                                msg_write.append(msg_text_plus + '\n')

                            except:
                                msg_text_box = i.find_element(By.XPATH,'.//*[starts-with(@id, "content-")]').get_attribute('aria-label')
                                msg_write.append(msg_text_box+'\n')
                                    
                                
                            for msg in msg_write:
                                long = False
                                if len(msg) > 60:
                                    long = True
                                    msg = textwrap.wrap(msg, width=60)   

                                if author != me_name:
                                    if long == True:
                                        for line in msg:
                                            f.write(line + '\n')
                                    else:
                                        f.write(msg)
                                else:
                                    if long == True:
                                        for line in msg:
                                            f.write(("{: >130}".format(line + '\n')))
                                    else:
                                        f.write("{: >130}".format(msg))
                        except:
                            
                            try:
                                div = i.find_element(By.XPATH,'.//div[starts-with(@class,"ui-divider__content")]').text
                            except:
                                div = i.find_element(By.XPATH, './/div[starts-with(@id,"control-message")]').text
                            finally:
                                if len(div) > 20:
                                    div = "User Action"
                                b_line = f"---------------------------------------------------------{div}-----------------------------------------------------------------"
                                f.write('\n' +b_line + '\n')

                    
                        
                    print(f"Archiving Chat with {name} complete!\n")
                    driver.switch_to.default_content()
                
                pull_msg(lis)
        driver.delete_all_cookies()
        print("All chats archived!")
        driver.quit()
    except:
        print("Something went wrong. (Or your internet was too slow) Try running this again.")
        driver.quit()
    
