def stationsTest(category: str, ID: int, file: str, region: str, splittedLine: list) -> None:
    if splittedLine[-5] == "" or splittedLine[-4] == "" or splittedLine[-3] == "" or splittedLine[-2] == "":
        print(f"Missing stations atribute in {category} --> {ID}.csv, source: {category} --> {region} --> {file}")