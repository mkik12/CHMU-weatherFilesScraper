import datetime
import os

from . import tests

def correctData(line: str) -> str:
    splittedLine = line.split(";")
    splittedLine = splittedLine[:4]

    if splittedLine[3] == "":
        return False
        # splittedLine[3] = "null"
    elif splittedLine[3].startswith("."):
        splittedLine[3] = "0" + splittedLine[3]
    elif splittedLine[3].startswith("-."):
        splittedLine[3] = "-0" + splittedLine[3][1:]

    newLine = ";".join(splittedLine)
    newLine += "\n"

    return newLine

def getData(lines: list, stations: list[tuple]) -> dict[int, list[str]]:
    stationData = {station[0]: [] for station in stations}

    data = False
    for line in lines:
        if line[:4] == "Rok;":
            data = True
            continue

        if data == True:
            splittedLine = line.split(";")
            dateLine = datetime.datetime(int(splittedLine[0]), int(splittedLine[1]), int(splittedLine[2]))

            for station in stations:

                startDateStation = datetime.datetime.strptime(station[3], "%Y-%m-%d")
                endDateStation = datetime.datetime.strptime(station[4], "%Y-%m-%d")

                if startDateStation <= dateLine <= endDateStation:
                    line = correctData(line)
                    if line is not False:
                        stationData[station[0]].append(line)
                    break

    return stationData

def getMetadata(category: str, file: str, ID: int, path: str, region) -> tuple:

    with open(os.path.join(path, file), "r") as text:
        lines = text.readlines()

    stations = []
    metadata = False

    for line in lines[:50]:

        if line[:10] == "Stanice ID":
            metadata = True
            continue

        if metadata == True:
            if line == "\n":
                break

            splittedLine = line.split(";")
            startDate = "-".join(splittedLine[2].split(".")[::-1])
            endDate = "-".join(splittedLine[3].split(".")[::-1])

            tests.stationsTest(category, ID, file, region, splittedLine)
            
            stations.append((ID, splittedLine[0],splittedLine[1], startDate, endDate, splittedLine[6].replace("\n", ""), splittedLine[4], splittedLine[5]))
            ID += 1

    return (ID, stations)