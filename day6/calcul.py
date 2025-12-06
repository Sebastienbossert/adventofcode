import os

class Calcul :
    """ Define a calcul """

    def __init__(self, new_number : int = None):

        """ Init function """
        self.list_of_number : list = []
        if new_number:
            self.list_of_number.append(new_number)
        self.operand = ""
        
    def defined_operand(self, operand : str):
        """ used to the define operand take in accompt """
        self.operand = operand

    def add_new_number(self, number: int):
        """ Add new number to the list """
        self.list_of_number.append(number)
    
    def made_the_calcul(self) -> int:
        """ Used to make the calcul, depending of the operand"""
        compteur = 0
        if self.operand == "+":
            # We have to make an addition
            for number in self.list_of_number:
                compteur += number
            return compteur
        elif self.operand == "*":
            # We have to make a multiplication
            first_occurence = True
            for number in self.list_of_number:
                if first_occurence:
                    compteur = number
                else:
                    compteur *= number
                first_occurence = False
            return compteur
        else:
            print("Bad things happend, or no operand found")
            return 0
        
class Calcul2 :
    """ Define a calcul for part 2"""

    def __init__(self, list_of_digit : list[str]):

        """ Init function """
        self.list_of_digit : list[str] = []
        for digit in list_of_digit:
            self.list_of_digit.append(digit)
        self.operand = ""

    def defined_operand(self, operand : str):
        """ used to the define operand take in accompt """
        self.operand = operand

    def add_new_list_of_digit(self, list_of_digit: list[str]):
        """ Add new number to the list """
        indice = 0
        for digit in list_of_digit:
            if (indice+1) <= len(self.list_of_digit):
                self.list_of_digit[indice] += digit
            else:
                self.list_of_digit.append(digit)
            indice += 1

    def list_of_number(self):
        # Remove 0 before
        """ Return in number, not str """
        list_of_digit_final = self.list_of_digit[0]
        list_without_0 = [x for x in list_of_digit_final if x != "0"]
        list_without_0_str = "".join(list_without_0)
        return int(list_without_0_str)
    
    def made_the_calcul(self) -> int:
        """ Used to make the calcul, depending of the operand"""
        compteur = 0
        if self.operand == "+":
            # We have to make an addition
            for number in self.list_of_digit:
                compteur += int(number)
            return compteur
        elif self.operand == "*":
            # We have to make a multiplication
            first_occurence = True
            for number in self.list_of_digit:
                if first_occurence:
                    compteur = int(number)
                else:
                    compteur *= int(number)
                first_occurence = False
            return compteur
        else:
            print("Bad things happend, or no operand found")
            return 0
    
def read_file(filename:str, filepath:str):
    """ Read database file given and calculate the result"""

    list_of_calc : list[Calcul] = []

    file_to_read = os.path.join(filepath,filename)
    with open(file_to_read, "r", encoding="utf-8") as fic:
        lines = fic.readlines()
        for line in lines:
            list_of_separated_number = line.split(" ")
            # Remove empty string from the list
            list_of_separated_number = [s for s in list_of_separated_number if s]
            list_of_separated_number = [s for s in list_of_separated_number if s != "\n"]
            if list_of_separated_number[0] != "+" and list_of_separated_number[0] != "*":
                if list_of_calc:
                    indice = 0
                    for number in list_of_separated_number:
                        if (indice + 1) <= len(list_of_calc):
                            list_of_calc[indice].add_new_number(int(number))
                        indice += 1
                else:
                    for number in list_of_separated_number:
                        list_of_calc.append(Calcul(int(number)))
            else:
                indice = 0
                for number in list_of_separated_number:
                    if (indice + 1) <= len(list_of_calc):
                        list_of_calc[indice].defined_operand(number)
                    indice += 1

    return list_of_calc

def read_file_2(filename:str, filepath:str):
    """ Read database file given and calculate the result"""

    list_of_calc : list[Calcul2] = []

    file_to_read = os.path.join(filepath,filename)
    with open(file_to_read, "r", encoding="utf-8") as fic:

        lines = fic.readlines()
        indice_of_line = 0

        dict_of_digit = {}

        for line in lines:

            list_of_separated_number = line.split(" ")

            # Remove empty string from the list

            list_of_separated_number = [s for s in list_of_separated_number if s != "\n"]
            list_of_separated_number_trimed = [s for s in list_of_separated_number if s]

            if list_of_separated_number_trimed[0] != "+" and list_of_separated_number_trimed[0] != "*":

                dict_of_digit[indice_of_line]= {}

                indice_of_list = 0

                for str_return in line:
                    if str_return != "\n":
                        dict_of_digit[indice_of_line][indice_of_list] = str_return
                        indice_of_list += 1


            indice_of_line += 1

    
        reverse_dict = {}
        for _, digito in dict_of_digit.items():
            for indice, value in digito.items():
                final_value = value
                if value.strip() == "":
                    for _ in value:
                        final_value = final_value + "0"
                if indice not in reverse_dict:
                    reverse_dict[indice] = final_value
                else:
                    reverse_dict[indice] = reverse_dict[indice] + final_value
                
        # Remove all blank from the dict and build all objects
        indice = 0
        dict_compare_calc = {}
        list_of_calc_inline = []
        for _,value_str in reverse_dict.items():
            if value_str :
                striped = [x for x in value_str if x.strip()]
                without_only_0 = [x for x in striped if x != '0']
                if without_only_0:
                    calcul = Calcul2(list_of_digit=[striped])
                    calcul.defined_operand(list_of_separated_number_trimed[indice])
                    list_of_calc_inline.append(calcul)
                else:
                    dict_compare_calc[indice] = list_of_calc_inline.copy()
                    list_of_calc_inline = []
                    indice+=1
        dict_compare_calc[indice] = list_of_calc_inline.copy()

        list_of_calc = []
        for _ , calcul_to_make in dict_compare_calc.items():
            newcalcul = Calcul()
            for calcul in calcul_to_make:
                newcalcul.add_new_number(calcul.list_of_number())
                newcalcul.defined_operand(calcul.operand)
            list_of_calc.append(newcalcul)

    return list_of_calc


def made_the_calcul(list_of_calcul : list):
    """ Used to make the calc of exercice 6 part 1"""
    compteur = 0
    for calcul in list_of_calcul:
        print(f"Adding {calcul.made_the_calcul()}")
        compteur += calcul.made_the_calcul()
    print(f"Réponse finale : {compteur}")


list_of_calc = read_file(filename="input_6.txt", filepath="/home/G5636/Téléchargements")
made_the_calcul(list_of_calcul=list_of_calc)
list_of_calc_2 = read_file_2(filename="input_6.txt", filepath="/home/G5636/Téléchargements")
made_the_calcul(list_of_calcul=list_of_calc_2)
