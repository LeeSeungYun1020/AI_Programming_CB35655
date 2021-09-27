def median():
    num_list = eval(input("Enter a number as list : "))
    if type(num_list) != list or len(num_list) == 0:
        return
    num_list.sort()
    mid = int(len(num_list)/2)
    med = num_list[mid]
    if len(num_list) % 2 == 0:
        med = (med + num_list[mid - 1]) / 2
    print("Median: {}".format(med))


if __name__ == '__main__':
    median()
