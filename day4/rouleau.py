""" Exercice 4 of adventofcode"""

import os

class Rouleau :

    """ Define a big stock of rouleau """

    def __init__(self, position_horizontal:int, position_vertical:int, is_a_rouleau:bool):

        """ Init function """

        self.horizontal_position = position_horizontal
        self.vertical_position = position_vertical

        self.is_a_rouleau = is_a_rouleau

    def get_if_a_rouleau_is_there(self):
        """ Return if this is a rouleau or not """
        return self.is_a_rouleau
    
    def get_horizontal_position(self):
        """ Return Horizontal position """
        return self.horizontal_position

    def get_vertical_position(self):
        """ Return Vertical position """
        return self.vertical_position
    
    def remove_rouleau(self):
        """ Remove the rouleau """
        self.is_a_rouleau = False


def read_file(filename:str, filepath:str):
    """ Read database file given and calculate the result"""

    dict_of_elevator = {}

    file_to_read = os.path.join(filepath,filename)
    with open(file_to_read, "r", encoding="utf-8") as fic:
        occurence_of_line = 0
        lines = fic.readlines()
        for line in lines:
            line = line.strip()
            list_of_str = list(line)
            placement_on_the_line = 0
            for rouleau_or_not in list_of_str:
                if occurence_of_line not in dict_of_elevator:
                    dict_of_elevator[occurence_of_line] = {}
                if rouleau_or_not == "@":
                    dict_of_elevator[occurence_of_line][placement_on_the_line] = Rouleau(position_vertical=occurence_of_line, position_horizontal=placement_on_the_line, is_a_rouleau=True)
                elif rouleau_or_not == ".":
                    dict_of_elevator[occurence_of_line][placement_on_the_line] = Rouleau(position_vertical=occurence_of_line, position_horizontal=placement_on_the_line, is_a_rouleau=False)
                else:
                    raise Exception("Wtf i am reading")
                placement_on_the_line+=1
            occurence_of_line+=1

    return dict_of_elevator

def check_adjacent(monrouleau : Rouleau, dict_of_elevator:dict):
    """ Used to check all adjacent"""

    left = [ monrouleau.get_vertical_position(), monrouleau.get_horizontal_position() -1 ]
    right = [ monrouleau.get_vertical_position(), monrouleau.get_horizontal_position() +1 ]
    top = [ monrouleau.get_vertical_position() - 1 , monrouleau.get_horizontal_position()]
    bottom = [ monrouleau.get_vertical_position() + 1 , monrouleau.get_horizontal_position()]
    bottom_right = [ monrouleau.get_vertical_position() + 1 , monrouleau.get_horizontal_position() + 1]
    bottom_left = [ monrouleau.get_vertical_position() + 1 , monrouleau.get_horizontal_position() -1]
    top_right = [ monrouleau.get_vertical_position() - 1 , monrouleau.get_horizontal_position() + 1 ]
    top_left = [ monrouleau.get_vertical_position() - 1 , monrouleau.get_horizontal_position() - 1 ]

    list_of_adjacent_to_check = [left,right,top,bottom,bottom_right,bottom_left,top_right,top_left]

    compteur = 0
    for ajacent_to_check in list_of_adjacent_to_check:
        if ajacent_to_check[0] in dict_of_elevator:
            if ajacent_to_check[1] in dict_of_elevator[ajacent_to_check[0]]:
                if dict_of_elevator[ajacent_to_check[0]][ajacent_to_check[1]].get_if_a_rouleau_is_there():
                    compteur += 1

    if compteur >= 4 :
        return False
    return True


def made_the_calcul_part_1(dict_of_elevator:dict):
    """ Used to made the calc of part 1 of exercice 4"""
    
    compteur = 0

    for key,_ in dict_of_elevator.items():
        for rouleau in dict_of_elevator[key].values():
            if rouleau.get_if_a_rouleau_is_there():
                retour = check_adjacent(monrouleau=rouleau,dict_of_elevator=dict_of_elevator)
                if retour:
                    compteur += 1

    print(compteur)

def made_the_calcul_part_2(dict_of_elevator:dict):
    """ Used to made the calc of part 2 of exercice 4"""
    
    compteur_final = 0
    compteur = 1

    while compteur != 0 :
        compteur = 0
        for key,_ in dict_of_elevator.items():
            for keyrouleau, rouleau in dict_of_elevator[key].items():
                if rouleau.get_if_a_rouleau_is_there():
                    retour = check_adjacent(monrouleau=rouleau,dict_of_elevator=dict_of_elevator)
                    if retour:
                        compteur += 1
                        dict_of_elevator[key][keyrouleau].remove_rouleau()
        compteur_final += compteur

    print(compteur_final)


dict_of_elevator = read_file(filename="input_4.txt", filepath="/home/G5636/Téléchargements")
made_the_calcul_part_1(dict_of_elevator=dict_of_elevator)
made_the_calcul_part_2(dict_of_elevator=dict_of_elevator)
