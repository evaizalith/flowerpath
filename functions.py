import csv

# Asks the user for text imput, validates the input, and returns it
def getStringInput():
    while True:
        try:
            userInput = str(input("Input a string: "))
            if (len(userInput) > 0):
                break
            print("Please input a non-empty string")
        except Exception:
            print("Please input a valid string")
    return userInput

# Takes a file name and text input
# Creates or adds the text to the associated file
def addToTxtFile(fileName: str, content: str):
    txtFile = open(fileName + ".txt", "a")
    txtFile.write(content)
    txtFile.close()
    return

# Takes a file name and 2D array input
# Creates or overrides the associated file with the array
def writeToCsvFile(fileName: str, inputs):
    with open(fileName + '.csv', 'w', newline='') as csvfile:
        fileWriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in inputs:
            fileWriter.writerow(row)
    return