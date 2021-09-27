def mortgage_calculations():
    annual_rate_interest = eval(input("annual rate of interest: "))
    monthly_payment = eval(input("Enter monthly payment: "))
    beg_balance = eval(input("Enter beg. of month balance: "))
    interest_paid_month, reduction_of_principal, month_balance = calculateValues(annual_rate_interest, monthly_payment, beg_balance)
    print("Interest paid for the month: ${:,.2f}".format(interest_paid_month))
    print("Reduction of principal: ${:,.2f}".format(reduction_of_principal))
    print("End of month balance: ${:,.2f}".format(month_balance))


def calculateValues(annualRateOfInterest, monthlyPayment, begBalance):
    """Calculate three monthly values associated with a mortgage
    Parameters
    ----------
    annualRateOfInterest : float
    Annual rate of interest
    monthlyPayment : float
    Monthly payment
    begBalance : float
    Beginning of month balance
    Returns
    -------
    (intForMonth, redOfPrincipal, endBalance)
    a tuple containing the following
    intForMonth : float
    Interest paid for the month
    redOfPrincipal : float
    Reduction of principal
    endBalance : float
    End of month balance
    """
    intForMonth = begBalance * annualRateOfInterest / 1200
    redOfPrincipal = monthlyPayment - intForMonth
    endBalance = begBalance - redOfPrincipal
    return (intForMonth, redOfPrincipal, endBalance)


if __name__ == '__main__':
    mortgage_calculations()