import os
import math

class Box :
    """ Define a Box """

    def __init__(self, x_position : int, y_position: int, z_position: int):

        """ Init function """
        self.x_position = x_position
        self.y_position = y_position
        self.z_position = z_position

class Circuit :
    """ Define a Circuit made of boxes"""

    def __init__(self) :
        """ Init function """
        self.dict_of_circuit = {}
        self.modelate_new_dict = {}
        self.populate_dict_value :  dict[Box] = {}
        self.indice_of_circuit = 0
        self.last_multiply = 0

    def add_new_circuit(self, box : Box):
        """ Used to add a new Circuit to the dict from a Box -> used to init"""
        self.dict_of_circuit[self.indice_of_circuit] = [box]
        self.indice_of_circuit += 1

    def distance_3d(self, box1: Box, box2: Box):
        """ Used to calculate distance between two point """
        d = math.sqrt((box2.x_position - box1.x_position)**2 + (box2.y_position - box1.y_position)**2 + (box2.z_position - box1.z_position)**2)
        return d
    
    def build_dict_of_distance(self):

        """ Used to make the dict of all distances """

        for key,list_of_box in self.dict_of_circuit.items():

            for box in list_of_box:

                actual_chiffre = key

                while actual_chiffre < len(self.dict_of_circuit.items()):

                    for boxes_compare in self.dict_of_circuit[actual_chiffre]:

                        if boxes_compare != box :

                            if box not in self.populate_dict_value:

                                self.populate_dict_value[box] = {}

                            self.populate_dict_value[box][boxes_compare] = self.distance_3d(box1 = box, box2 = boxes_compare)

                    actual_chiffre += 1

    def made_junction_2(self):

        """ Used to make junction of all circuit """

        if not self.populate_dict_value:
            self.build_dict_of_distance()
        
        min_value = None
        association_to_fuse = []

        for box1, box2 in self.populate_dict_value.items():

            if not min_value:
                min_value = min(box2.values())
                for key, value in box2.items():
                    if value == min_value:
                        association_to_fuse = [box1,key]
            
            else:

                if min_value > min(box2.values()):
                    min_value = min(box2.values())
                    for key, value in box2.items():
                        if value == min_value:
                            association_to_fuse = [box1,key]
    
        # Remove from the dict of valor
        if association_to_fuse[0] in self.populate_dict_value.keys():
            if association_to_fuse[1] in self.populate_dict_value[association_to_fuse[0]]:
                self.populate_dict_value[association_to_fuse[0]].pop(association_to_fuse[1])

        # Try to fusion
        circuit_to_fuse1 = None
        circuit_to_fuse2 = None

        for circuiter, list_of_box in self.dict_of_circuit.items():
            if association_to_fuse[0] in list_of_box:
                circuit_to_fuse1 = circuiter
            if association_to_fuse[1] in list_of_box:
                circuit_to_fuse2 = circuiter

        if circuit_to_fuse1 != circuit_to_fuse2:
            self.dict_of_circuit[circuit_to_fuse1] += self.dict_of_circuit[circuit_to_fuse2].copy()
            self.dict_of_circuit.pop(circuit_to_fuse2)

        list_of_len = []

        for circuit in self.dict_of_circuit.values():

            list_of_len.append(len(circuit))

        self.last_multiply = 1
        if list_of_len.count(1) == 0:
            for mescouilles in association_to_fuse:
                self.last_multiply*=mescouilles.x_position
            return True
        
        return False
    
    def made_junction(self, limit : int):

        """ Used to make junction of all circuit """

        if not self.populate_dict_value:
            self.build_dict_of_distance()
        
        min_value = None
        association_to_fuse = []

        for box1, box2 in self.populate_dict_value.items():

            if not min_value:
                min_value = min(box2.values())
                for key, value in box2.items():
                    if value == min_value:
                        association_to_fuse = [box1,key]
            
            else:

                if min_value > min(box2.values()):
                    min_value = min(box2.values())
                    for key, value in box2.items():
                        if value == min_value:
                            association_to_fuse = [box1,key]
        
        # Remove from the dict of valor
        if association_to_fuse[0] in self.populate_dict_value.keys():
            if association_to_fuse[1] in self.populate_dict_value[association_to_fuse[0]]:
                self.populate_dict_value[association_to_fuse[0]].pop(association_to_fuse[1])

        # Try to fusion
        circuit_to_fuse1 = None
        circuit_to_fuse2 = None

        for circuiter, list_of_box in self.dict_of_circuit.items():
            if association_to_fuse[0] in list_of_box:
                circuit_to_fuse1 = circuiter
            if association_to_fuse[1] in list_of_box:
                circuit_to_fuse2 = circuiter

        if circuit_to_fuse1 != circuit_to_fuse2:
            self.dict_of_circuit[circuit_to_fuse1] += self.dict_of_circuit[circuit_to_fuse2].copy()
            self.dict_of_circuit.pop(circuit_to_fuse2)

        

        return 1


    def made_the_final_calc(self):
        """ Used to make the final calc of exercie 8 part 1 """

        list_of_len = []

        for circuit in self.dict_of_circuit.values():

            list_of_len.append(len(circuit))

        top1 = 0
        top2 = 0
        top3 = 0

        for taille in list_of_len:
            if top1 <= taille :
                top3 = top2
                top2 = top1
                top1 = taille
            elif top2 <= taille:
                top3 = top2
                top2 = taille
            elif top3 < taille:
                top3 = taille
                
        list_of_len_top3 = [top1, top2, top3]
        return_final = None

        for tall in list_of_len_top3:
            if return_final:
                return_final *= tall
            else:
                return_final = tall

        print(return_final)


def read_file(filename:str, filepath:str):
    """ Read database file given and calculate the result"""

    new_circuit = Circuit()

    file_to_read = os.path.join(filepath,filename)
    with open(file_to_read, "r", encoding="utf-8") as fic:
        lines = fic.readlines()
        for line in lines:
            line = line.strip()
            position = line.split(",")
            new_box = Box(x_position=int(position[0]), y_position=int(position[1]), z_position=int(position[2]))
            new_circuit.add_new_circuit(new_box)
            
    return new_circuit

def made_the_calcul_for_example(circuit : Circuit):

    """ Used to make the calc of exercice 7 part 1"""
    
    i = 0

    while i < 10:

        occurence = circuit.made_junction(limit = i - 10 )
        i+=occurence

    circuit.made_the_final_calc()

def made_the_calcul(circuit : Circuit):

    """ Used to make the calc of exercice 7 part 1"""
    
    i = 0

    while i < 1000:

        occurence = circuit.made_junction(limit = i - 1000 )
        i+=occurence

    circuit.made_the_final_calc()

def made_the_calcul2(circuit : Circuit):

    """ Used to make the calc of exercice 7 part 1"""
    
    finish = False

    while not finish:

        finish = circuit.made_junction_2()

    print(circuit.last_multiply)


circuit = read_file(filename="input_8.txt", filepath="/home/G5636/Téléchargements")
made_the_calcul2(circuit=circuit)
