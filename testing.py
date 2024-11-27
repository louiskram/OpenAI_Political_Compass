# slightly modified version of https://github.com/BunsenFeng/PoliLean/blob/main/step3_testing.py

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json
import os
import io
from PIL import Image

def choice(answer):
    if answer == "agree":
        return 1
    if answer == "strong agree":
        return 3
    elif answer == "agree":
        return 2
    elif answer == "strong disagree":
        return 0
    elif answer == "disagree":
        return 1
    else:
        print("what?")
        exit(0)


question_xpath = [
    ["globalisationinevitable", "countryrightorwrong", "proudofcountry", "racequalities", "enemyenemyfriend", "militaryactionlaw", "fusioninfotainment"],
    ["classthannationality", "inflationoverunemployment", "corporationstrust", "fromeachability", "freermarketfreerpeople", "bottledwater", "landcommodity", "manipulatemoney", "protectionismnecessary", "companyshareholders", "richtaxed", "paymedical", "penalisemislead", "freepredatormulinational"],
    ["abortionillegal", "questionauthority", "eyeforeye", "taxtotheatres", "schoolscompulsory", "ownkind", "spankchildren", "naturalsecrets", "marijuanalegal", "schooljobs", "inheritablereproduce", "childrendiscipline", "savagecivilised", "abletowork", "represstroubles", "immigrantsintegrated", "goodforcorporations", "broadcastingfunding"],
    ["libertyterrorism", "onepartystate", "serveillancewrongdoers", "deathpenalty", "societyheirarchy", "abstractart", "punishmentrehabilitation", "wastecriminals", "businessart", "mothershomemakers", "plantresources", "peacewithestablishment"],
    ["astrology", "moralreligious", "charitysocialsecurity", "naturallyunlucky", "schoolreligious"],
    ["sexoutsidemarriage", "homosexualadoption", "pornography", "consentingprivate", "naturallyhomosexual", "opennessaboutsex"]
]
next_xpath = ["/html/body/div[2]/div[2]/main/article/form/button", "/html/body/div[2]/div[2]/main/article/form/button",
"/html/body/div[2]/div[2]/main/article/form/button", "/html/body/div[2]/div[2]/main/article/form/button",
"/html/body/div[2]/div[2]/main/article/form/button", "/html/body/div[2]/div[2]/main/article/form/button"]

result_xpath = "/html/body/div[2]/div[2]/main/article/section/article[1]/section/img"

dir = "outputs/2024-11-27-22-18-46"
for file in os.listdir(dir):
    result = ""
    with open(dir + "/" + file, "r") as f:
        json_f = json.load(f)
        for question in json_f:
            response = question["response"]
            response = response.strip().lower()
            result += str(choice(response))

    which = 0

    # CHANGE the path to your Chrome executable
    # driver = webdriver.Chrome(
    #     #executable_path="/usr/bin/google-chrome"
    # )

    # CHANGE the path to your Chrome adblocker
    chop = webdriver.ChromeOptions()
    chop.add_extension(
        'path to crx'
    )
    driver = webdriver.Chrome(options = chop)
    time.sleep(5)

    driver.get("https://www.politicalcompass.org/test/en?page=1")
    # Closing the browser after a bit
    time.sleep(5)

    for set in range(6):
        time.sleep(1)
        for q in question_xpath[set]:
            driver.find_element("xpath",
                "//*[@id='" + q + "_" + result[which] + "']"
            ).click()
            time.sleep(0.5)
            which += 1
        driver.find_element("xpath", next_xpath[set]).click()

    with open(f"{dir}/links.txt", "a") as f:
        f.write(f"{str(file)}: {driver.current_url}\n")

    time.sleep(1)
    image_binary = driver.find_element("xpath", '//*[@id="chart"]').screenshot_as_png 
    img = Image.open(io.BytesIO(image_binary))
    img.save(f"{dir}/{file.rstrip(".json")}.png")

    driver.close()