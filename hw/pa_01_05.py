def pay_raise():
    first_name, last_name = input_name()
    salary = input_salary()
    salary = calculate_new_salary(salary)
    display_new_salary(first_name, last_name, salary)


def input_name():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    return first_name, last_name


def input_salary():
    return eval(input("Enter current salary: "))


def calculate_new_salary(current_salary):
    if current_salary < 40000:
        return current_salary * 1.05
    else:
        return current_salary + (current_salary - 40000) * 0.02 + 2000


def display_new_salary(first_name, last_name, salary):
    print("New salary for {} {}: ${:,.2f}".format(first_name, last_name, salary))


if __name__ == '__main__':
    pay_raise()
