def change_in_salary():
    salary = eval(input("Enter beginning salary: "))
    new_salary = salary * (1.1 ** 3)
    print("New salary: ${:,.2f}".format(new_salary))
    print("Change: {:.2%}".format(new_salary/salary - 1))

change_in_salary()