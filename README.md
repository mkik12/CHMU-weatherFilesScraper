# CHMI – Meteorological Data

*Copyright (C) 2025  Mikuláš Kadečka - mikulas.kad@seznam.cz*

All of the included scripts, accessible from the root directory, are used to download and process meteorological data files from the webpage of the Czech Hydrometeorological Institute. **The programs must be run in the order listed below!**

The programs and their descriptions are as follows:

1. web_scraping: **main.py** 

   - Downloads all meteorological files from the CHMI dynamic webpage.
   - Stores them in the "DATA_CHMU" folder, which will be located in the root directory, maintaining the same folder structure as on the CHMI webpage.
   - Approximately 6,500 files (1.1 GB) will be downloaded, and the script takes roughly 3 hours to run.

2. data_processing: **unzip.py**
   
   - Extracts all downloaded meteorological files in the "DATA_CHMU" directory while preserving the folder hierarchy.

3. data_processing: **preparation.py** 
   
   - Extracts all useful information from the meteorological files and stores it in the "output" folder, which will be located in the root directory.
   - The original folder structure is simplified.
   - Creates category folders and stores station files (will be used to create a point layer) and measurement files (tables containing measurements, linked to stations through their name and fileID in the station file).

4. data_processing: **transformation.py**
   
   - Converts all files in the "output" directory to GPKG format and saves them in the "spatial_data" directory.
   - Corrects the attribute data types.
   - This program is intended to be run in the QGIS application (requires the Processing plugin and additional functionalities).

## Dependencies

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip install selenium
pip install undetected-chromedriver
pip install zipfile36
```

## License

[GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.html)