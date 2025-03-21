# This program transforms the format of the downloaded and processed files.
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
from qgis import processing
from qgis.core import QgsCoordinateReferenceSystem

mainFolderPath = "C:\\ ... \\download_prepare_data" # Please set your own path.

categories = ["Průměrná denní teplota vzduchu", 
              "Maximální denní teplota vzduchu", 
              "Minimální denní teplota vzduchu", 
              "Průměrná denní relativní vlhkost vzduchu", 
              "Denní úhrn srážek", 
              "Výška nově napadlého sněhu", 
              "Celková výška sněhové pokrývky", 
              "Denní úhrn doby trvání slunečního svitu", 
              "Průměrný denní tlak vzduchu", 
              "Průměrná denní rychlost větru", 
              "Maximální rychlost větru", 
              "Globální záření"]

dataPath = os.path.join(mainFolderPath, "output")
outputPath = os.path.join(mainFolderPath, "spatial_data")
os.mkdir(outputPath)

for i, category in zip(range(len(categories)), categories):

    outputCategoryPath = os.path.join(outputPath, str(i))
    workingPath = os.path.join(dataPath, category)

    os.mkdir(outputCategoryPath)

    files = os.listdir(workingPath)

    for file in files:

        if file != "removed_files.txt" and file != "stations.csv":
            pass
            processing.run("native:refactorfields",{
                    'INPUT': os.path.join(workingPath, file),
                    'FIELDS_MAPPING': [
                        # {
                        #     'expression': "make_date(\"year\", \"month\", \"day\")", 'length': 0, 'name': 'date',
                        #     'precision': 0, 'sub_type': 0, 'type': 14, 'type_name': 'date'},
                        {
                            'expression': '"year"', 'length': 0, 'name': 'year',
                            'precision': 0, 'sub_type': 0, 'type': 2, 'type_name': 'integer'},
                        {
                            'expression': '"month"', 'length': 0, 'name': 'month',
                            'precision': 0, 'sub_type': 0, 'type': 2, 'type_name': 'integer'},
                        {
                            'expression': '"day"', 'length': 0, 'name': 'day',
                            'precision': 0, 'sub_type': 0, 'type': 2, 'type_name': 'integer'},
                        {
                            'expression': '"value"', 'length': 0, 'name': 'value',
                            'precision': 0, 'sub_type': 0, 'type': 6, 'type_name': 'double precision'}
                        ],
                    'OUTPUT': os.path.join(outputCategoryPath, file[:-4] + ".gpkg")})
        
        elif file == "stations.csv":  
            table = processing.run("native:createpointslayerfromtable",{
                    'INPUT': os.path.join(workingPath, file),
                    'XFIELD': 'longtitude',
                    'YFIELD': 'latitude',
                    'ZFIELD': 'height',
                    'MFIELD': '',
                    'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:4326'),
                    'OUTPUT': "TEMPORARY_OUTPUT"})
            
            processing.run("native:refactorfields", {
                    'INPUT': table["OUTPUT"],
                    'FIELDS_MAPPING': [

                        {
                            'expression': '"fileID"', 'length': 0, 'name': 'fileID',
                            'precision': 0, 'sub_type': 0, 'type': 2, 'type_name': 'integer'},
                        {
                            'expression': '"stationID"', 'length': 0, 'name': 'stationID',
                            'precision': 0, 'sub_type': 0, 'type': 10, 'type_name': 'text'},
                        {
                            'expression': '"name"', 'length': 0, 'name': 'name',
                            'precision': 0, 'sub_type': 0, 'type': 10, 'type_name': 'text'},
                        {
                            'expression': '"start"', 'length': 0, 'name': 'start',
                            'precision': 0, 'sub_type': 0, 'type': 14, 'type_name': 'date'},
                        {
                            'expression': '"end"', 'length': 0, 'name': 'end',
                            'precision': 0, 'sub_type': 0, 'type': 14, 'type_name': 'date'},
                        {
                            'expression': '"height"', 'length': 0, 'name': 'height',
                            'precision': 0, 'sub_type': 0, 'type': 6, 'type_name': 'double precision'},
                        {
                            'expression': '"longtitude"', 'length': 0, 'name': 'longitude',
                            'precision': 0, 'sub_type': 0, 'type': 6, 'type_name': 'double precision'},
                        {
                            'expression': '"latitude"', 'length': 0, 'name': 'latitude',
                            'precision': 0, 'sub_type': 0, 'type': 6, 'type_name': 'double precision'}
                        ],
                    'OUTPUT': os.path.join(outputCategoryPath, "stations.gpkg")})