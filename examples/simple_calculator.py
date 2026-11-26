first_number = 0
second_number = 0
operation = ''
result = 0.0
print('===== SIMPLE CALCULATOR =====')
first_number = int(input('Enter the first number: '))
second_number = int(input('Enter the second number: '))
operation = input('Choose operation (+, -, *, /): ')
if (operation == '+'):
    result = (first_number + second_number)
else:
    if (operation == '-'):
        result = (first_number - second_number)
    else:
        if (operation == '*'):
            result = (first_number * second_number)
        else:
            if (operation == '/'):
                if (second_number != 0):
                    result = (first_number / second_number)
                else:
                    print('Error: Cannot divide by zero.')
            else:
                print('Invalid operation.')
print('===== CALCULATION RESULT =====')
print(result)
