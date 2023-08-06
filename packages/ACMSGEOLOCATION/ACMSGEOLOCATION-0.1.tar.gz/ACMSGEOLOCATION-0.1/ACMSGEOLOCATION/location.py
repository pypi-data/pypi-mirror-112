import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from twilio.rest import Client
import webbrowser
import requests
from PIL import Image
from pytesseract import pytesseract

class location():
    def __init__(self,url_of_Ip_webcam,path_to_tesseract):
        self.URL=str(url_of_Ip_webcam)
        self.path_to_tesseract=str(path_to_tesseract)
    def get_location(self):
        #print(self.URL+"/"+"sensors.html")
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get(self.URL+"/"+"sensors.html")
        time.sleep(10)
        checkboxElement = driver.find_element_by_id("gpscb")
        status=checkboxElement.is_selected()
        if(status):
            pass
        else:
            checkboxElement.click()
        time.sleep(10)
        S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
        driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment
        driver.find_element_by_tag_name('body').screenshot('web_screenshot.png')
        driver.quit()
        # Defining paths to the image we would be using
        image_path = r"web_screenshot.png"
          
        # Opening the image & storing it in an image object
        img = Image.open(image_path)
          
        # Providing the tesseract executable location to pytesseract library
        pytesseract.tesseract_cmd = self.path_to_tesseract
          
        # Passing the image object to image_to_string() function. This function will extract the text from the image
        text = pytesseract.image_to_string(img)
        #print(text)
        str1=[]
        akmstr=[]
        if("Get location" in text[:-1]):
            akm=text.index("Get location")
            for i in (text[(akm):]):
                if(i.isdigit() or i=="."):
                    str1.append(i)
        for i in range(len(str1)):
            if(str1[i]=="."):
                akmstr.append(i)
        #print(akmstr)
        url1=str(str1[akmstr[0]-2])+str(str1[akmstr[0]-1])+'.'+str("".join(str1[(akmstr[0]+1):(akmstr[0]+6)]))
        url2=str(str1[akmstr[1]-2])+str(str1[akmstr[1]-1])+'.'+str("".join(str1[(akmstr[1]+1):(akmstr[1]+6)]))
        url=(f"https://www.google.com/maps/search/?api=1&query={url1},{url2}")
        return url

def main():
    obj=location(url_of_Ip_webcam,path_to_tesseract=r"C:\Program Files\Tesseract-OCR\tesseract.exe")
    #obj=location("http://192.168.43.121:8080",path_to_tesseract=r"C:\Program Files\Tesseract-OCR\tesseract.exe")
    url=obj.get_location()
    #print(url)
if __name__=="__main__":
    main()
