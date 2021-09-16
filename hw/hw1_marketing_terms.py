def marketing_terms():
    purchase_price = eval(input("Enter purchase price: "))
    selling_price = eval(input("Enter selling price: "))
    markup = selling_price - purchase_price
    percentage_markup = markup/purchase_price
    profit_margin = markup/selling_price

    print("Markup: ${0:.1f}".format(markup))
    print("Percentage markup: {0:.1%}".format(percentage_markup))
    print("Profit margin: {0:.2%}".format(profit_margin))

marketing_terms()