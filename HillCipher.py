import sys

def letter_to_number(letter):
    if letter == default_letter:
        return 0
    elif alphabet == "Z":
        return ord(letter) - ord("A") + 1
    elif alphabet != "":
        return alphabet.index(letter)
    else:
        return ord(letter) - ord("A")

def number_to_letter(number):
    if number == 0:
        return default_letter
    elif alphabet == "Z":
        return chr(ord("A") + number - 1)
    elif alphabet != "":
        return alphabet[number]
    else:
        return chr(ord("A") + number)

def determinant(key_matrix):
    return (key_matrix[0] * key_matrix[3] - key_matrix[1] * key_matrix[2]) % mod

def mod_mult_inverse(det):
    try:
        return pow(det, -1, mod)
    except ValueError:
        return None 

def mod_inverse_matrix(key_matrix, mmi):
    inverse_key = [key_matrix[3], -key_matrix[1], -key_matrix[2], key_matrix[0]]
    for x in range(4):
        inverse_key[x] = (inverse_key[x] * mmi) % mod
    
    return inverse_key

def encryption_and_decryption(initial_text, mod, matrix):
    output_text = ""

    if len(initial_text) % 2 == 1:
        initial_text += default_letter

    vectors = []
    for letter in range(0, len(initial_text), 2):
        first_char = letter_to_number(initial_text[letter])
        second_char = letter_to_number(initial_text[letter + 1])

        vectors.append(matrix[0] * first_char + matrix[1] * second_char)
        vectors.append(matrix[2] * first_char + matrix[3] * second_char)

    for number in range(len(vectors)):
        vectors[number] %= mod
        output_text += number_to_letter(vectors[number])

    return output_text

def get_live_matrix():
    print("[ [ _ ], [ _ ] ]")
    print("[ [ _ ], [ _ ] ]")

    UP = "\033[A"
    
    matrix = []
    
    # Row 1, Col 1
    sys.stdout.write(UP * 2 + "\r" + "\033[4C") 
    sys.stdout.flush()
    number = int(input())
    if number is not None:
        matrix.append(number)
    
    # Row 1, Col 2
    sys.stdout.write(UP + "\r" + "\033[11C")
    sys.stdout.flush()
    number = int(input())
    if number is not None:
        matrix.append(number)
    
    # Row 2, Col 1
    sys.stdout.write("\r" + "\033[4C")
    sys.stdout.flush()
    number = int(input())
    if number is not None:
        matrix.append(number)

    # Row 2, Col 2
    sys.stdout.write(UP + "\r" + "\033[11C")
    sys.stdout.flush()
    number = int(input())
    if number is not None:
        matrix.append(number)

    return matrix

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

#### MAIN PROGRAM ####

while True:
    ## VARIABLES ##

    plaintext = ""
    key_matrix = []
    det = None

    ciphertext = ""
    inverse_key_matrix = []
    mmi = None

    mod = 26
    alphabet = ""
    default_letter = "A"
    allCaps = True

    ## PROGRAM ##

    print("\nHill Cipher Calculator\n")

    custom = input("Use Custom Alphabet? y/N: ")

    if str.upper(custom) == "Y":
        print("\ntype EXIT to finish,\ntype CAPS to enable case sensitive text,\ntype HELP to print this message.\n")

        index = 0
        while True:
            invalidated = False

            if index == 0:
                letter = input(f"Input the letter that maps to {index}: ")
            else:
                letter = input(f"{index} ↦ ")

            if str.upper(letter) == "HELP":
                print("\ntype EXIT to finish,\ntype CAPS to enable case sensitive text,\ntype HELP to print this message.\n")
                continue
            elif str.upper(letter) == "CAPS":
                allCaps = False
                continue
            elif str.upper(letter) == "EXIT":
                break
            elif str(letter).isalpha():
                history = int(letter)
                if history > index:
                    invalidated = True
                else:
                    index = history
                    continue
            
            if len(letter) > 1 or len(letter) == 0 or invalidated:
                print("\nInvalid character selection.\n")
                continue

            if allCaps:
                if len(alphabet) >= index + 1:
                    alphabet[index] = str.upper(letter)
                else:
                    alphabet += str.upper(letter)
            else:
                if len(alphabet) >= index + 1:
                    alphabet[index] = letter
                else:
                    alphabet += letter

            index += 1

        mod = len(alphabet)
    elif str.upper(custom) == "Z": ## Preset with Z as 0
        alphabet = "Z"
        default_letter = "Z"

        mod = 26
    else:
        print("Using standard 26 letter alphabet, A ↦ 0 ... Z ↦ 25.")
        mod = 26

    while True:
        plaintext = input("\nInput plaintext, return if unknown: ")
        ciphertext = input("Input ciphertext, return if unknown: ")

        if allCaps == True:
            plaintext = str.upper(plaintext)
            ciphertext = str.upper(ciphertext)

        if plaintext == "" and ciphertext == "":
            print("\nAt least one type of text required to find the other!")
            continue
        elif len(plaintext) > 0 and len(ciphertext) > 0 and len(plaintext) != len(ciphertext):
            print("\nPlaintext and Ciphertext must contain the same amount of letters.")
            continue
        else:
            break

    valid_matrix = False
    while valid_matrix == False:
        ## if plaintext == "" or ciphertext == "":
        ##     print("Input key matrix: ")
        ## else:
        ##     print("Input key matrix, return if unknown: \n")
        print("Input key matrix: ")

        key_matrix = get_live_matrix()

        if len(key_matrix) < 4:
            print("\nInvalid matrix: value cannot be null.")
            continue

        det = determinant(key_matrix) % mod

        if det == 0:
            print("\nInvalid matrix: determinant cannot be 0.\n")
            continue

        # Modular check: If GCD is 1, they share NO prime factors (works for any mod size)
        if gcd(det, mod) == 1:
            mmi = mod_mult_inverse(det)
            if mmi is not None:
                valid_matrix = True
            else:
                print("\nInvalid matrix: Determinant has no modular inverse.\n")
        else:
            print(f"\nInvalid matrix: Determinant shares a factor with {mod}.\n")


    mmi = mod_mult_inverse(det)
    inverse_key_matrix = mod_inverse_matrix(key_matrix, mmi)

    if key_matrix == []:
        print("")

    if plaintext == "":
        plaintext = encryption_and_decryption(ciphertext, mod, inverse_key_matrix)

    if ciphertext == "":
        ciphertext = encryption_and_decryption(plaintext, mod, key_matrix)

    if len(plaintext) % 2 != 0:
        plaintext += default_letter
    
    print("\nPlaintext: " + plaintext)
    print("Ciphertext: " + ciphertext)
    print("Key matrix: " + str(key_matrix))

    selection = input("\nRun once more? y/N: ")

    if str.upper(selection) != "Y":
        break