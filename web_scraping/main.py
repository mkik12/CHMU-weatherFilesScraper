# This program downloads meteorological files from the webpage of the Czech Hydrometeorological Institute.
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

import copy
import os
import time

from functions import *
from helper_lists import *

referenceDistrict = copy.deepcopy(NUTS3)
folderPath = getWorkingPath(__file__)

os.makedirs(folderPath, exist_ok=True)
writeBeginningOfMetadata(folderPath)

errorCount = 0

while categories:

    try:

        if not referenceDistrict:
            categories.pop(0)
            referenceDistrict = copy.deepcopy(NUTS3)

        os.makedirs(os.path.join(folderPath, categories[0]), exist_ok=True)

        workingPath = os.path.join(folderPath, categories[0], referenceDistrict[0])
        os.makedirs(workingPath, exist_ok=True)

        driver = setupChromeDriver(workingPath)
        driver.get("https://www.chmi.cz/historicka-data/pocasi/denni-data/Denni-data-dle-z.-123-1998-Sb")
        sleep(3)

        dismissCookie(driver)

        findAndClickOnElement(driver, categories[0], 1)
    
        findAndClickOnElement(driver, referenceDistrict[0], 1)

        nOfAvailable = downloadData(driver, workingPath)
        if nOfAvailable == 0 and categories[0] != "Globální záření":
            continue
    
        driver.close()
        writeMetadata(folderPath, categories[0], referenceDistrict[0], nOfAvailable, len(os.listdir(workingPath)))
        referenceDistrict.pop(0)

    except Exception as e:
        try:
            driver.close()
        except:
            pass
        print(f"Error '{type(e).__name__}' occurred. No need to restart the script, downloading is continuing.")
        errorCount += 1

        if errorCount > 19:
            ended = True
            print("The script was stopped due to too many occurred errors. Please restart the script.")
            try:
                driver.close()
            except:
                pass
            break
if ended is True:
    writeEndOfMetadata(folderPath)