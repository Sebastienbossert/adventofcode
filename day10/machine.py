import os
import threading

class Machine  :

    """ Define a Machine """

    def __init__(self, indicator_light_diagrams : list[str], button_wiring_schematics: list[list[int]], joltage_requirement: list[int]):

        """ Init function """

        self.indicator_light_diagram : list[bool] = [True if s == "#" else False for s in indicator_light_diagrams]

        self.button_wiring_schematics : list[list[int]] = button_wiring_schematics

        self.joltage_requirements : list[int] = joltage_requirement

    
    def checking_if_two_list_are_equals(self, list1 : list[bool], list2 : list[bool]) -> bool:
        """ Check if two list of bool are equals """

        equals = True
        # First check if counter of False are equals 
        if list1.count(False) == list2.count(False):
            indice = 0
            while indice < len(list1):
                if not list1[indice] == list2[indice]:
                    equals = False
                    break
                indice += 1
        else :
            equals = False

        return equals
    
    def checking_if_two_list_are_equals_int(self, list1 : list[int], list2 : list[int]) -> bool:
        """ Check if two list of bool are equals """

        equals = True
        # First check if counter of False are equals 
        indice = 0
        for int_number in list1:
            if list2[indice] != int_number:
                equals=False
            indice+=1
        
        return equals

    def part_1(self):

        """ Just do the part 1 of day 10; with no joltage attached """

        goal = self.indicator_light_diagram
        acutal_list : list[bool] = [False for s in self.indicator_light_diagram.copy()]
        list_niveau : list[list[bool]] = []
        list_niveau.append(acutal_list)

        is_not_finish = True
        pressed_button = 0

        # Format the based dict for example
        # We are at level indice_of_niveau = 0

        """
        new_list_niveau = []
        for list in list_niveau:
        """

        # First we have to determinate new value list from actual_list after applicating every indicator light diagrams
        """ 
        actual_list_to_apply = actual_list.copy()
        for schema in self.button_wiring_schematics :
                for button_to_turn in schema :
                    actual_list_to_apply[button_to_turn] = True if not actual_list_to_apply[button_to_turn] else False
        """
        # On check ensuite le resultat
        """ 
        if checking_if_two_list_are_equals(list1 = actual_list_to_apply; list2=goal):
            is_not_finish = True
            break
        else:
            new_list_niveau.append(actual_list_to_apply)
        """
        # Et on fini finalement par écraser l'ancienne list_niveau si on a pas trouvé à celui-ci la réponse
        """
        list_niveau = new_list_niveau
        """
        # Puis on return l'indice de sortie pour savoir le nombre d'occurence qu'on a eu pour en arriver la 

        while is_not_finish:
            new_list_niveau : list[list[bool]]= []
            for list_l in list_niveau:
                for schema in self.button_wiring_schematics:
                    acutal_list_to_apply = list_l.copy()
                    for button_to_turn in schema:
                        acutal_list_to_apply[button_to_turn] = True if not acutal_list_to_apply[button_to_turn] else False
                    if self.checking_if_two_list_are_equals(list1=acutal_list_to_apply, list2=goal):
                        is_not_finish = False
                    else:
                        new_list_niveau.append(acutal_list_to_apply.copy())
            
            pressed_button +=1
            list_niveau=new_list_niveau.copy()

        return pressed_button
    
    def part_2(self):
        """ brut force"""
        """ Just do the part 2 of day 10; with joltage attached """
        """ We have to reduce the number of things to count to make it work like part1"""

        goal = self.joltage_requirements
        acutal_list : list[int] = [0 for s in self.joltage_requirements.copy()]
        list_niveau : dict[tuple[int]] = {}
        already_existed_dict = {}
        list_niveau[tuple(acutal_list)] = self.button_wiring_schematics

        is_not_finish = True
        pressed_button = 0
        keep_in_memory = {}

        net_max_level_to_reach  = goal.copy()
        indice_max = self.determinate_max_level_indice_to_reach_first(level=net_max_level_to_reach)

        while is_not_finish:
            
            new_list_niveau : dict[tuple[int]] = {}
            transition = False

            for list_l, schematic in list_niveau.items():

                reproduce_schema = schematic.copy()

                for schema in schematic:

                    acutal_list_to_apply = list(list_l).copy()
                    if indice_max in schema or indice_max == -1:
                        for button_to_turn in schema:
                            # On ajoute 1 au bouton, sauf si il correspond déjà à notre max
                            if acutal_list_to_apply[button_to_turn]!= goal[button_to_turn]:
                                acutal_list_to_apply[button_to_turn] += 1
                            # Si il correspond à notre max; le schéma n'a plus matière à être check, on break et on remove le schema
                            else:
                                if schema in reproduce_schema:
                                    reproduce_schema.remove(schema)

                    if self.checking_if_two_list_are_equals_int(list1=acutal_list_to_apply, list2=goal):
                        is_not_finish = False
                    else:
                        
                        # Remove bad list of number, no need to keep something who reach more than something we tract
                        indice_list_number = 0
                        need_to_keep = True
                        for integral_number in acutal_list_to_apply:
                            if goal[indice_list_number] < integral_number:
                                need_to_keep = False
                            indice_list_number+=1
                        

                        actu_dict_global = already_existed_dict.copy()
                        actu_dict = actu_dict_global
                        # If we already passed on it

                        already_exist = True
                        leveling = 0
                        for int_checking in acutal_list_to_apply:
                            if int_checking in actu_dict.keys():
                                # We have to reach the bigger first, but without trepassing the other 
                                if indice_max == leveling:
                                    # Check too if the int_checking is the moste elevated or not (reach gain)
                                    if (int_checking >= (max(actu_dict.keys()) if actu_dict.keys() else 0) and int_checking <= self.joltage_requirements[leveling]):
                                        if int_checking == self.joltage_requirements[leveling]:
                                            transition = True
                                        actu_dict = actu_dict[int_checking]
                                        already_exist=True
                                        leveling += 1
                                    else:
                                        already_exist=True
                                        break
                                else:
                                    actu_dict = actu_dict[int_checking]
                                    leveling += 1
                            else:
                                already_exist = False
                                actu_dict[int_checking] = {}
                                actu_dict = actu_dict[int_checking]
                                leveling += 1

                        already_existed_dict = actu_dict_global
                        
                        # exclude useless stuff

                        if need_to_keep and not already_exist:
                            new_list_niveau[tuple(acutal_list_to_apply.copy())] = reproduce_schema
            
            if transition:
                indice_max = self.determinate_max_level_indice_to_reach_first(level=net_max_level_to_reach)
            # Si on atteint pas le bout des valeurs possibles en reprenant le maximum
            if new_list_niveau:
                keep_in_memory[pressed_button] = list_niveau.copy()
                pressed_button+=1
                list_niveau=new_list_niveau.copy()
            else:
                pressed_button -= 1
                list_niveau=keep_in_memory[pressed_button]
            
        return pressed_button
    
    def determinate_max_level_indice_to_reach_first(self,level : list[int]):

        """ Determinate the max level to reach first"""
        max_to_reach = -1
        max_indice = 0
        indice = 0

        for s in level:
            if s > max_to_reach:
                max_to_reach = s
                max_indice = indice
            indice += 1

        level[max_indice] = -1

        if max_to_reach == -1:
            return -1

        return max_indice
    
def do_all_calcul_part_1(list_of_machine : list[Machine]):
    """ Do the calcul of part 1 of Day 10 """
    compteur_of_niveau = 0
    for machine in list_of_machine:
        compteur_of_niveau+=machine.part_1()
    print(compteur_of_niveau)

def do_all_calcul_part_2(list_of_machine : list[Machine]):
    """ Do the calcul of part 1 of Day 10 """
    compteur_of_niveau = 0
    list_of_thread : list[threading.Thread]= []

    for machine in list_of_machine:

        thead = threading.Thread(target=machine.part_2())
        list_of_thread.append(thead)
    
    for thread in list_of_thread:
        thread.start()

    for thread in list_of_thread:
        compteur_of_niveau += thread.join()

    print(compteur_of_niveau)

def read_file(filename:str, filepath:str):
    """ Read database file given and calculate the result"""

    list_of_machine : list[Machine] = []

    file_to_read = os.path.join(filepath,filename)

    with open(file_to_read, "r", encoding="utf-8") as fic:

        lines = fic.readlines()

        for line in lines:

            line = line.strip()
            position = line.split(" ")
            
            # Light diagrams
            indicator_light_diagrams = position[0].split("[")
            indicator_light_diagrams = indicator_light_diagrams[1].split("]")[0]

            # Schematics 
            button_wiring_schematics = []
            int_occurence = 1
            while int_occurence + 1 < len(position):
                remove_parenthese = position[int_occurence].split("(")[1]
                remove_parenthese = remove_parenthese.split(")")[0]
                button_wiring_schematics.append([int(s) for s in remove_parenthese.split(",")])
                int_occurence += 1
            
            # Joltage requirement
            remove_dict = position[int_occurence].split("{")[1]
            remove_dict = remove_dict.split("}")[0]

            joltage_requirement = [int(s) for s in remove_dict.split(",")]

            new_machine = Machine(indicator_light_diagrams=indicator_light_diagrams, button_wiring_schematics=button_wiring_schematics, joltage_requirement=joltage_requirement)
            list_of_machine.append(new_machine)         
        
    return list_of_machine

list_of_machine = read_file(filename="input_10.txt", filepath="/home/G5636/Téléchargements")
do_all_calcul_part_2(list_of_machine=list_of_machine)
