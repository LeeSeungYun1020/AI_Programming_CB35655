def populateDictionary():
    file = open("hw3_units.txt", "r")
    p_dict = {}
    for line in file:
        name, number = line.split(',')
        p_dict[name] = float(number)
    file.close()
    return p_dict

def getInput():
    origin = input("Unit to convert from: ")
    destination = input("Unit to convert to: ")
    length = eval(input("Enter length in {}: ".format(origin)))
    return origin, destination, length

def main():
    feet = populateDictionary()
    orig, dest, length = getInput()
    ans = length * feet[orig] / feet[dest]
    print("Length in {0}: {1:,.4f}".format(dest, ans))
main()