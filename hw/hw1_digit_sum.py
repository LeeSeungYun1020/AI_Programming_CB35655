def digit_sum():
    sum = 0
    for i in range(1000001):
        for j in str(i):
            sum += int(j)
    print("The sum of the digits in the numbers")
    print("from {} to one million is {:,}".format(1, sum))


digit_sum()
