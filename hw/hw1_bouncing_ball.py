def bouncing_ball():
    coefficient = eval(input("Enter coefficient of restitution: "))
    height = eval(input("Enter initial height in meters: "))
    bounce = 0
    traveled = 0
    while height >= 0.1:
        traveled += height
        height *= coefficient
        bounce += 1
        traveled += height
    traveled -= height
    print("Number of bounces: ", bounce)
    print("Meters traveled: {:.2f}".format(traveled))

bouncing_ball()