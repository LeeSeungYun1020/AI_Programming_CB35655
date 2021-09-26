def bouncing_ball():
    coefficient = eval(input("Enter coefficient of restitution: "))
    height = eval(input("Enter initial height in meters: "))

    bounces = 0
    traveled = 0
    while height >= 0.1:
        bounces += 1
        traveled += height
        height *= coefficient
        traveled += height
    traveled -= height

    print("Number of bounces:", bounces)
    print("Meters traveled: {:.2f}".format(traveled))


if __name__ == '__main__':
    bouncing_ball()
