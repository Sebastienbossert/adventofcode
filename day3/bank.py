""" Exercice 3 of adventofcode"""

import os

class Bank :

    """ Bank of digit """

    def __init__(self, list_of_digit : list[str]):
        self.list_of_digit = list_of_digit

    def calculate_joltage(self):
        """ Function used to calculate the joltage"""

        first_digit = 0
        second_digit = 0

        compteur_of_digit = 0

        for digit in self.list_of_digit:
            digit_int = int(digit)
            if digit_int > first_digit and ( compteur_of_digit + 1 )< len(self.list_of_digit):
                # if the first digit change, the second digit return to 0
                print(f"Replace first digit by {digit_int}")
                first_digit = digit_int
                second_digit = 0
            elif digit_int > second_digit :
                print(f"Replace second digit by {digit_int}")
                second_digit = digit_int
            compteur_of_digit+=1

        print(f"Return this digit for this bank :  {first_digit}{second_digit}")
        return int(f"{first_digit}{second_digit}")

    def calculate_joltage_2(self):
        """ Function used to calculate the joltage for exercice 2 """

        list_of_joltage = [0,0,0,0,0,0,0,0,0,0,0,0]

        compteur_of_digit = 0

        for digit in self.list_of_digit:
            digit_int = int(digit)
            compteur_of_occurence = 0
            while compteur_of_occurence < len(list_of_joltage) :
                if list_of_joltage[compteur_of_occurence] < digit_int and (compteur_of_digit + (12 - (compteur_of_occurence + 1) )) < len(self.list_of_digit):
                    list_of_joltage[compteur_of_occurence] = digit_int
                    # We have to reinit he list after this occurence
                    reinit_int = compteur_of_occurence + 1
                    while reinit_int < len(list_of_joltage):
                        list_of_joltage[reinit_int] = 0
                        reinit_int +=1
                    break
                compteur_of_occurence += 1
            compteur_of_digit+=1
        new_list = [str(digit) for digit in list_of_joltage]
        string_value = "".join(new_list)
        int_final = int(string_value)
        print(f"Return this digit for this bank :  {int_final}")
        return int(f"{int_final}")


def read_file(filename:str, filepath:str):
    """ Read database file given and calculate the result"""

    table_of_bank = []

    file_to_read = os.path.join(filepath,filename)
    with open(file_to_read, "r", encoding="utf-8") as fic:
        lines = fic.readlines()
        for line in lines:
            line = line.strip()
            new_bank = Bank(list(line))
            table_of_bank.append(new_bank)

    return table_of_bank

def made_the_calcul_part_1(banks:list):
    """ Used to made the calc of part 1 of exercice 3"""
    int_final = 0
    for bank in banks:
        joltage = bank.calculate_joltage()
        int_final += joltage
    print(int_final)

def made_the_calcul_part_2(banks:list):
    """ Used to made the calc of part 1 of exercice 3"""
    int_final = 0
    for bank in banks:
        joltage = bank.calculate_joltage_2()
        int_final += joltage
    print(int_final)

table_of_bank = read_file(filename="input_3.txt", filepath="/home/G5636/Téléchargements")
made_the_calcul_part_1(table_of_bank)
made_the_calcul_part_2(table_of_bank)
