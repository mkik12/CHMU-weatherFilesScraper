import os

from . import parsing

def writeData(category: str, file: str, outputPath: str, region: str, stations: list, workingPath: str) -> None:

    stationsToRemove = []

    with open(os.path.join(workingPath, file), "r") as text:
        lines = text.readlines()
    
    stationData = parsing.getData(lines, stations)
    
    for ID, lines in stationData.items():
        if len(lines) != 0:
            with open(os.path.join(outputPath, f"{ID}.csv"), "a") as text:
                text.write("year;month;day;value\n")
                text.writelines(lines)
        else:
            with open(os.path.join(outputPath, "removed_files.txt"), "a") as text:
                text.write(f"file: {category} --> {ID}.csv;source: {category} --> {region} --> {file}\n")
            stationsToRemove.append(ID)
    
    return stationsToRemove

def writeStations(path: str, stations: list) -> None:
    outputPath = os.path.join(path, "stations.csv")
    if os.path.exists(outputPath):
        with open(outputPath, "a") as text:
            [text.write(f"{station[0]};{station[1]};{station[2]};{station[3]};{station[4]};{station[5]};{station[6]};{station[7]}\n") for station in stations]
    else:
        with open(outputPath, "w") as text:
            text.write("fileID;stationID;name;start;end;height;longtitude;latitude\n")
            [text.write(f"{station[0]};{station[1]};{station[2]};{station[3]};{station[4]};{station[5]};{station[6]};{station[7]}\n") for station in stations]