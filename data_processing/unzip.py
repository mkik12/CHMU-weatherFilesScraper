# This program unzips downloaded files located in the "DATA_CHMU" folder.
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

from functions import *

import time

t1 = time.time()

workingPath = utils.getWorkingPath(__file__)

for category in os.listdir(workingPath):

    if os.path.isdir(os.path.join(workingPath, category)):
        for region in os.listdir(os.path.join(workingPath, category)):
            
            if os.path.isdir(os.path.join(workingPath, category, region)):
                for file in os.listdir(os.path.join(workingPath, category, region)):
                    utils.unZip(os.path.join(workingPath, category, region), file)

t2 = time.time()

print(f"Task took: {t2 - t1}s.")