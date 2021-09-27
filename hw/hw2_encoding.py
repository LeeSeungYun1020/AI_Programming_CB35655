def encoding():
    input_list = eval(input("Input list = "))
    count_dict = {0: 0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
    for i in input_list:
        count_dict[i] += 1
    # print("Encoded list =", list(count_dict.items()))
    print("Encoded list =", [list(it) for it in count_dict.items()])


if __name__ == '__main__':
    encoding()
