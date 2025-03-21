# Functions from this module are used in "main.py".
# Copyright (C) 2025 by Mikuláš Kadečka - mikulas.kad@seznam.cz  

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
from selenium.webdriver.common.by import By
from time import sleep, strftime, localtime
import undetected_chromedriver as uc

def dismissCookie(driver: uc.Chrome) -> None:
    # /html/body/div[3]/div/div[1]/div/div[2]/button[1]
    cookieButton = driver.find_element(By.XPATH, '//*[@id="c-s-bn"]')
    cookieButton.click()

def downloadData(driver: uc.Chrome, workingPath: str) -> int:
    contentsFromDir = os.listdir(workingPath)
    elements = [x.get_attribute("innerText") for x in driver.find_elements(By.PARTIAL_LINK_TEXT, ".zip")]
    elements = list(set(elements))
    repetitionCount = 0

    while len(elements) != len(os.listdir(workingPath)):
        repetitionCount += 1

        for name in elements:
            if name not in contentsFromDir:
                e = driver.find_element(By.LINK_TEXT, name)
                e.click()
                sleep(1)

        contentsFromDir = []
        for item in os.listdir(workingPath):
            if item in elements:
                contentsFromDir.append(item)
            else:
                os.remove(os.path.join(workingPath, item))
        if repetitionCount > 9:
            return Exception
    sleep(5)
    return len(contentsFromDir)

def findAndClickOnElement(driver: uc.Chrome, text: str, time: int) -> None:
    element = driver.find_element(By.LINK_TEXT, text)
    element.click()
    sleep(time)

def getWorkingPath(scriptPath: object) -> str:
    workingPath = os.path.abspath(scriptPath)
    workingPath = os.path.dirname(os.path.dirname(workingPath))
    workingPath = os.path.join(workingPath, "DATA_CHMU")

    return workingPath

def isDownloaded(workingPath: str) -> None:
    wait = True
    while wait:
        sleep(1)
        wait = False
        for file in os.listdir(workingPath):
            if file.endswith(".crdownload"):
                wait = True

def setupChromeDriver(workingPath: str) -> None:
        """Function to set up Chrome driver with a specific download directory."""

        chromeOptions = uc.ChromeOptions()
        prefs = {
            "download.default_directory": workingPath,
            "download.prompt_for_download": False,
            "directory_upgrade": True,
            "safebrowsing.enabled": True,
            "profile.default_content_settings.popups": 0,
            "profile.content_settings.exceptions.automatic_downloads.*.setting": 1
        }
        chromeOptions.add_experimental_option("prefs", prefs)

        return uc.Chrome(options = chromeOptions)

def writeBeginningOfMetadata(path: str) -> None:
    with open(os.path.join(path, "metadata.csv"), "w") as metadata:
        currentTime = strftime("%H:%M:%S", localtime())
        metadata.write(f"Current time:;{currentTime}\n")
        metadata.write("Location;nOfAvailable;nOfDownloaded\n")

def writeEndOfMetadata(path: str) -> None:
    with open(os.path.join(path, "metadata.csv"), "a") as metadata:
        currentTime = strftime("%H:%M:%S", localtime())
        metadata.write(f"Current time:;{currentTime}\n")

def writeMetadata(path: str, type: str, place: str, nOfAvailable: int, nOfDownloaded: int) -> None:
    with open(os.path.join(path, "metadata.csv"), "a") as metadata:
        metadata.write(f"{type} - {place};{nOfAvailable};{nOfDownloaded}\n")