# slightly modified version of https://github.com/BunsenFeng/PoliLean/blob/main/step3_testing.py

import argparse
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
import re

import tqdm.contrib

def choice(answer):
    # some gpt-models style theirs answers
    # remove any non whitespace or other characters
    answer = re.sub(r'[^a-zA-Z\s]', '', answer)

    if answer == "strongly agree":
        return 3
    elif answer == "agree":
        return 2
    elif answer == "disagree":
        return 1
    elif answer == "strongly disagree":
        return 0
    else:
        print(answer)
        return -1

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

# Return the path of the newest directory within the specified parent directory
parent_directory = "outputs/"
subdirs = [os.path.join(parent_directory, d) for d in os.listdir(parent_directory) if os.path.isdir(os.path.join(parent_directory, d))]
newest_subdir = max(subdirs, key=os.path.getmtime)

# Read in input dir over command line
# Use newest directory in parent_directory if no argument is given
parser = argparse.ArgumentParser(description="Enter statements on Political Compass Test.")
parser.add_argument('--directory', type=str, default=newest_subdir, help='Input directory path')
args = parser.parse_args()
input_directory = args.directory or os.path.join(parent_directory, newest_subdir)

dir = input_directory
for i, file in tqdm.contrib.tenumerate(os.listdir(dir)):
    result = ""
    with open(os.path.join(dir, file), "r") as f:
        json_f = json.load(f)
        for question in json_f:
            response = question["response"]
            response = response.strip().lower()
            response = choice(response)
            if response >= 0:
                result += str(response)
            else:
                print(file)
                break
        else:
            which = 0

            # CHANGE the path to your Chrome adblocker
            chop = webdriver.ChromeOptions()
            chop.add_argument("--headless=new")
            chop.add_extension(
                'CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_61_2_0.crx'
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

            time.sleep(3)
            image_binary = driver.find_element("xpath", '//*[@id="SvgjsSvg1001"]').screenshot_as_png 
            img = Image.open(io.BytesIO(image_binary))
            img.save(f"{dir}/{file.rstrip(".json")}.png")

            driver.close()
