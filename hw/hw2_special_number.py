def special_number():
    for i in range(1000, 10000):
        reversed_num = int("".join((reversed(str(i)))))
        if i * 4 == reversed_num:
            print("Since 4 × {0} is {1},\nthe special number is {1}".format(i, reversed_num))


if __name__ == '__main__':
    special_number()
