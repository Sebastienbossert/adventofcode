""" Exercice 4 of adventofcode"""

import os

class Range :

    """ Range of id ok """

    def __init__(self, lower_range:int, uper_range:int):

        """ Init function """

        self.lower_range = lower_range
        self.uper_range = uper_range

    def check_if_in_range(self, number: int):
        """ Return if number in range or not """
        return (number >= self.lower_range and number <= self.uper_range)
    
    def set_lower_range(self, number: int):
        """ SETTER """
        self.lower_range = number

    def set_upper_range(self, number: int):
        """ SETTER """
        self.uper_range = number
    
    def return_number_in_range(self) -> int:
        """ Return compteur of all number in the range """
        print(f"entre ({self.lower_range},{self.uper_range}) il y a {(self.uper_range - self.lower_range) + 1}")
        return (self.uper_range - self.lower_range) + 1


class Ingredient :

    """ Define an ingredient with his id """

    def __init__(self, id : int):

        """ Init function """

        self.id = id

    def get_id(self) -> int:
        """ Getter of id"""
        return self.id


def read_file(filename:str, filepath:str):
    """ Read database file given and calculate the result"""

    list_of_range = []
    list_of_ingredient = []

    file_to_read = os.path.join(filepath,filename)
    with open(file_to_read, "r", encoding="utf-8") as fic:
        lines = fic.readlines()
        fresh_id_ranges = True
        for line in lines:
            line = line.strip()
            if line == "":
                fresh_id_ranges = False
            else:
                if fresh_id_ranges:
                    split_line = line.split("-")
                    new_range = Range(lower_range=int(split_line[0]), uper_range = int(split_line[1]))
                    list_of_range.append(new_range)
                else:
                    read_number=int(line)
                    ingredient = Ingredient(read_number)
                    list_of_ingredient.append(ingredient)

    return list_of_range, list_of_ingredient

def made_the_calcul_part_1(list_of_range : list[Range], list_of_ingredient : list[Ingredient]):
    """ Used to made the calc of part 1 of exercice 5"""
    
    compteur = 0

    for ingredient in list_of_ingredient:
        for range in list_of_range:
            if range.check_if_in_range(ingredient.get_id()):
                print(f"Ingredient id {ingredient.get_id()} in range of ({range.lower_range},{range.uper_range})")
                compteur += 1
                break
    print(compteur)

def made_the_calcul_part_2(list_of_range : list[Range]):
    """ Used to made the calc of part 2 of exercice 5"""
    
    compteur = 0
    # We gonna recreate a new list of range, erased of same value
    new_list_of_range : list[Range] = list()
    new_list_of_range.append(list_of_range[0])
    for range in list_of_range:
        copy_list = new_list_of_range.copy()
        new_range = Range(range.lower_range, range.uper_range)
        for keep_in_mind_old_rotate in copy_list:
            if keep_in_mind_old_rotate.lower_range > new_range.lower_range and keep_in_mind_old_rotate.lower_range < new_range.uper_range and keep_in_mind_old_rotate.uper_range < new_range.uper_range:
                new_list_of_range.remove(keep_in_mind_old_rotate)
            elif keep_in_mind_old_rotate.uper_range < new_range.uper_range and keep_in_mind_old_rotate.uper_range > new_range.lower_range:
                new_range.set_lower_range(new_range.lower_range)
                new_list_of_range.remove(keep_in_mind_old_rotate)
        new_list_of_range.append(new_range)
    for new_range in new_list_of_range:
        print(f"My new range : ({new_range.lower_range},{new_range.uper_range})")
        compteur += new_range.return_number_in_range()
    print(compteur)


list_of_range, list_of_ingredient = read_file(filename="input_5.txt", filepath="/home/G5636/Téléchargements")
made_the_calcul_part_1(list_of_range=list_of_range, list_of_ingredient=list_of_ingredient)
made_the_calcul_part_2(list_of_range=list_of_range)
