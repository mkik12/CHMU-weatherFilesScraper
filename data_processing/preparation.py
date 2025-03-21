# This program processes unzipped files from the "DATA_CHMU" folder.
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

dataPath = utils.getWorkingPath(__file__, "DATA_CHMU")
outputPath = utils.getWorkingPath(__file__, "output")
os.mkdir(outputPath)

folderCombinations = utils.getCombinations(categories, regions)
ID = 0

for combination in folderCombinations:

    category = combination[0]
    region = combination[1]

    outputCategoryPath = os.path.join(outputPath, category)
    try:
        os.mkdir(outputCategoryPath)
        ID = 0
    except FileExistsError:
        pass

    workingPath = os.path.join(dataPath, category, region)
    files = os.listdir(workingPath)

    for file in files:
        metadata = parsing.getMetadata(category, file, ID, workingPath, region)

        ID = metadata[0]
        stations = metadata[1]

        stationsToRemove = writing.writeData(category, file, outputCategoryPath, region, stations, workingPath)

        stations = utils.stationsRemoval(stations, stationsToRemove)

        writing.writeStations(outputCategoryPath, stations)