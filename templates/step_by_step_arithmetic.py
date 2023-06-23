
def add_large_numbers(num1, num2):
    # convert numbers to strings for easy manipulation
    str_num1 = str(num1)
    str_num2 = str(num2)

    # Make the numbers of same length
    len_diff = len(str_num1) - len(str_num2)
    if len_diff > 0:
        str_num2 = '0' * len_diff + str_num2
    elif len_diff < 0:
        str_num1 = '0' * (-len_diff) + str_num1

    # Add zeros at the beginning of result and carry for alignment purposes
    result = '0' * (len(str_num1) + 1)
    carry = '0' * (len(str_num1) + 1)

    for i in range(len(str_num1)-1, -1, -1):
        temp_result = int(str_num1[i]) + int(str_num2[i])
        if carry[i+1] != '0':
            temp_result += int(carry[i+1])
        carry = carry[:i] + str(temp_result // 10) + carry[i+1:]
        result = result[:i+1] + str(temp_result % 10) + result[i+2:]
        print("\nCarry: ", carry)
        print("Partial result: ", result)

    # print the final result removing leading zeros
    print("\nFinal result: ", int(result))

# Test the function
add_large_numbers(1234, 5678)

