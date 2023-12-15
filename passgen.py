import random

PASS_LEN = 12

def gen_pass():
    char_number = [1, 1, 1, 1] # lower_letter, upper_letters, numbers, symbols

    # Add +1 item per iteration to a random group
    for _ in range(len(char_number), PASS_LEN):
        rnd_index = random.randint(0, len(char_number) - 1)
        char_number[rnd_index] += 1

    # Write all lower case english chars into the list
    lower_chars = []
    for value in range(97, 123):
        lower_chars.append(chr(value))

    # Write all upper case english chars into the list
    upper_chars = []
    for value in range(65, 91):
        upper_chars.append(chr(value))
        
    number_chars = []
    for value in range(0, 10):
        number_chars.append(str(value))
        
    symbol_chars = ['!', '#', '$', '(', ')', '%', '&', '*', '+']
        
    result = []

    group_index = 0
    for _ in range(0, PASS_LEN):
        if char_number[group_index] == 0:
            group_index += 1
            
        char_number[group_index] -= 1

        if group_index == 0:
            result.append(random.choice(lower_chars))
        elif group_index == 1:
            result.append(random.choice(upper_chars))
        elif group_index == 2:
            result.append(random.choice(number_chars))
        elif group_index == 3:
            result.append(random.choice(symbol_chars))
        
    random.shuffle(result)
    result = ''.join(result)

    return result
