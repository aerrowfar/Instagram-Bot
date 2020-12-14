from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class InstaBot:
    #initialize class variables.
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()

    #closes web broswer.
    def closeBrowser(self):
        self.driver.close()

    #Logs the user in.
    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(2)
        login_button = driver.find_element_by_xpath("/html/body/span/section/main/article/div[2]/div[2]/p/a")
        login_button.click()
        time.sleep(2)

        #Find and fill in username.
        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.click()
        user_name_elem.send_keys(self.username)

        #Find and fill in password.
        password_elem = driver.find_element_by_xpath("//input[@name='password']")
        password_elem.clear()
        password_elem.click()
        password_elem.send_keys(self.password)

        #Find and click the Login button.
        login_button_two = driver.find_element_by_xpath("/html/body/span/section/main/div/article/div/div[1]/div/form/div[3]/button")
        login_button_two.click()
        time.sleep(3)

    # Likes the top 65 photos in a given hashtag.
    def like_photo_by_tag(self,hashtag):
        driver = self.driver
        #Go to the hashtag page.
        driver.get("https://www.instagram.com/explore/tags/"+ hashtag +"/")
        time.sleep(2)

        #Scroll down twice so we have more images.
        for i in range(1,3):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(2)

        #Grab all elemnts with the 'href' xpath tag into an array.
        hrefs=driver.find_elements_by_xpath("//a[@href]")
        #Go through array and grab the url value from each href.
        pic_hrefs = [elem.get_attribute('href') for elem in hrefs]

        #Prints how many photos are available in the page.
        print(hashtag + ' photos: ' + str(len(pic_hrefs)))

        #Go through the url array and open each url.
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

            #Find the click button by XPath and click it.
            #Uses 12 seconds of sleep to satisfy the Instagram limit of 350 likes per hour.
            try:
                driver.find_element_by_xpath("//span[@aria-label='Like']").click()
                time.sleep(12)

            #If that didnt work, print and error message..
            except Exception as e:
                print("not found")
                time.sleep(2)


    #Download a user's images.
    def download_user_pics(self,user_name):
        driver = self.driver
        #Open that user's page.
        driver.get("https://www.instagram.com/"+user_name+"/")
        time.sleep(2)
        #Scroll down thrice.
        for i in range(1,4):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(2)

        #Grab all elemnts with the 'href' xpath tag into an array.
        #FOund a bunch of shit that wasnt relevant, but finally went through pics.
        hrefs=driver.find_elements_by_xpath("//a[@href]")

        #Go through array and grab the url value from each href.
        pic_hrefs = [elem.get_attribute('href') for elem in hrefs]

        #Prints how many photos are available in the page.
        print('photos found: ' + str(len(pic_hrefs)))

        # Clean up all the bullshit urls that are not relevant.
        pic_page_urls = [k for k in pic_hrefs if 'instagram.com/p/' in k]


        #Go through the url array and open each url.
        for x in pic_page_urls:
            driver.get(x)
            time.sleep(3)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")


            #Find image URL:

            try:
                #1st method of getting it.
                image_url_location = driver.find_element_by_xpath("/html/body/span/section/main/div/div/article/div[1]/div/div/div[1]/img")
                image_url = image_url_location.get_attribute('src')
                print(image_url)
            except:
                try:
                    #second method of getting it if that didnt work.
                    image_url_location = driver.find_element_by_xpath("/html/body/span/section/main/div/div/article/div[1]/div/div/div/div[1]/img")
                    image_url = image_url_location.get_attribute('src')
                    print(image_url)

                #must be an album.
                except:
                    try:
                    #grabs album image.
                        try:
                            #first way of getting img.
                            image_url_location = driver.find_element_by_xpath("/html/body/span/section/main/div/div/article/div[1]/div/div/div/div[2]/div/div[1]/div/ul/li[1]/div/div/div/div/div[1]/img")
                            image_url = image_url_location.get_attribute('src')
                            print(image_url)
                        except:
                            try:
                                #if it didnt work, try the second way of getting img.
                                image_url_location = driver.find_element_by_xpath("/html/body/span/section/main/div/div/article/div[1]/div/div/div/div[2]/div/div[1]/div/ul/li[1]/div/div/div/div[1]/img")
                                image_url = image_url_location.get_attribute('src')
                                print(image_url)
                            except:
                                print("Failed to get an album image.")
                                pass


                    except:
                        print("Failed to get an image.")
                        pass








#Running the script.
nameIG = InstaBot("user,"pass")
nameIG.login()