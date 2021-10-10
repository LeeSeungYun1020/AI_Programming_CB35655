def readSetFromFile():
    file = open("hw3_names.txt", "r")
    name_list = [item for item in file]
    file.close()
    return set(name_list)

def inputName():
    return input("Enter name to be included: ") + '\n'

def insertSet(mySet, name):
    mySet.add(name)
    return mySet

def writeToFile(modifiedSet):
    file = open("hw3_names.txt", "w")
    for it in sorted(modifiedSet):
        file.write(it)
    file.close()

def main():
    mySet = readSetFromFile()
    name = inputName()
    modifiedSet = insertSet(mySet, name)
    writeToFile(modifiedSet)

main()