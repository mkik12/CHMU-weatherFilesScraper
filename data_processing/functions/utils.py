import os
import zipfile as z

def getWorkingPath(scriptPath: object, folder: str) -> str:
    workingPath = os.path.abspath(scriptPath)
    workingPath = os.path.dirname(os.path.dirname(workingPath))
    workingPath = os.path.join(workingPath, folder)


    return workingPath

def getCombinations(categories: list, regions: list) -> list[tuple]:

    combinations = []

    for type in categories:
        for place in regions:
            combinations.append((type, place))
    return combinations

def stationsRemoval(stations: tuple, stationsToRemove: list) -> tuple:

    newStations = []

    for station in stations:

        if int(station[0]) not in stationsToRemove:
            newStations.append(station)

    return (newStations)

def unZip(workingPath: str, file: str) -> tuple:
        zipPath = os.pathjoin(workingPath, file)
        if zipPath.endswith(".zip"):
            with z.ZipFile(zipPath) as f:
                f.extractall(path=workingPath)
            os.remove(zipPath)