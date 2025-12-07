import os

class Beam :
    """ Define a Beam """

    def __init__(self, horizontal_position, vertical_position):

        """ Init function """
        self.horizontal_position = horizontal_position
        self.vertical_position = vertical_position

    def get_position(self) -> (int, int):
        """ Getter of actual position of the beam """
        return (self.vertical_position, self.horizontal_position)
    
    def move_forward(self):
        """ Used to make the beam move to the new horizontal position """
        self.vertical_position += 1

class Table :

    """ Define the table where all beam will continue there travel"""

    def __init__(self):
        
        self.indice_of_maximal_line = 0
        self.dict_of_manifold = {}
        self.list_of_beam : list[Beam] = []
        self.compteur_of_split = 0
        self.dict_of_manifold_compteur = {}

    def increment_dict(self, dict_of_line : dict):

        """ Used to increment the dict with a new line"""

        for key,value in dict_of_line.items():
            # Find all starters Beam
            if value == "S":
                starterbeam = Beam(vertical_position=self.indice_of_maximal_line, horizontal_position=key)
                self.list_of_beam.append(starterbeam)

        self.dict_of_manifold[self.indice_of_maximal_line] = dict_of_line
        self.indice_of_maximal_line +=1

    def move_forward_in_table(self):

        """ Used to make Beam move in the table """

        # If beam encounter a separator, we have to cancel it

        list_of_beam_to_use = self.list_of_beam
        indice_of_parcours = 0

        while (indice_of_parcours + 1) < self.indice_of_maximal_line:

            new_list_of_beam = []

            for beam in list_of_beam_to_use:

                beam.move_forward()
                vertical_position, horizontal_position = beam.get_position()

                if self.dict_of_manifold[vertical_position][horizontal_position] == "^":
                    # Create two new Beam
                    # Verify first if a beam is not already in the position of this one
                    if not self.verify_already_occuped(newlist_of_beam=new_list_of_beam, horizontal_position=horizontal_position + 1):
                        new_list_of_beam.append(Beam(vertical_position=vertical_position, horizontal_position=horizontal_position + 1 ))
                    # Verify secondly if a beam is not already in the position of this one
                    if not self.verify_already_occuped(newlist_of_beam=new_list_of_beam, horizontal_position=horizontal_position - 1):
                        new_list_of_beam.append(Beam(vertical_position=vertical_position, horizontal_position=horizontal_position - 1 ))
                    self.compteur_of_split += 1
                else:
                    if not self.verify_already_occuped(newlist_of_beam=new_list_of_beam, horizontal_position=horizontal_position):
                        new_list_of_beam.append(beam)

            indice_of_parcours += 1
            list_of_beam_to_use = new_list_of_beam.copy()
        
        return self.compteur_of_split
    
    def move_forward_in_table_quantum(self, new_beam : Beam = None, repriseparcours : int = 0):

        """ Used to make Beam move in the table, recursive function """

        nombre_embranchement = 1

        # Is beam set ? 
        if new_beam:
            beam_to_use = new_beam
        else:
            beam_to_use = self.list_of_beam[0]

        # We come from there
        indice_of_parcours = repriseparcours

        while (indice_of_parcours + 1) < self.indice_of_maximal_line:

            # We make the beam move forward
            beam_to_use.move_forward()
            vertical_position, horizontal_position = beam_to_use.get_position()

            # If we get a seperator

            if self.dict_of_manifold[vertical_position][horizontal_position] == "^":

                # Vertical part
                
                if vertical_position in self.dict_of_manifold_compteur :

                    # Left part

                    nombre_embranchement = 0

                    if horizontal_position - 1 in self.dict_of_manifold_compteur[vertical_position]:

                        nombre_embranchement += self.dict_of_manifold_compteur[vertical_position][horizontal_position - 1]

                    else:

                        nombre_embranche_left = self.move_forward_in_table_quantum(new_beam=Beam(vertical_position=vertical_position, horizontal_position=horizontal_position - 1 ), repriseparcours=indice_of_parcours+1)
                        self.dict_of_manifold_compteur[vertical_position][horizontal_position - 1] = nombre_embranche_left
                        nombre_embranchement += nombre_embranche_left


                    # Right part

                    if horizontal_position + 1 in self.dict_of_manifold_compteur[vertical_position]:

                        nombre_embranchement += self.dict_of_manifold_compteur[vertical_position][horizontal_position + 1]

                    else:

                        nombre_embranche_right = self.move_forward_in_table_quantum(new_beam=Beam(vertical_position=vertical_position, horizontal_position=horizontal_position + 1 ), repriseparcours=indice_of_parcours+1)
                        self.dict_of_manifold_compteur[vertical_position][horizontal_position + 1] = nombre_embranche_right
                        nombre_embranchement += nombre_embranche_right
                    
                    break

                # If no vertical part actually exist

                else:

                    self.dict_of_manifold_compteur[vertical_position] = {}

                    nombre_embranche_right = self.move_forward_in_table_quantum(new_beam=Beam(vertical_position=vertical_position, horizontal_position=horizontal_position + 1 ), repriseparcours=indice_of_parcours+1)
                    nombre_embranche_left = self.move_forward_in_table_quantum(new_beam=Beam(vertical_position=vertical_position, horizontal_position=horizontal_position - 1 ), repriseparcours=indice_of_parcours+1)

                    self.dict_of_manifold_compteur[vertical_position][horizontal_position - 1] = nombre_embranche_left
                    self.dict_of_manifold_compteur[vertical_position][horizontal_position + 1] = nombre_embranche_right

                    nombre_embranchement = nombre_embranche_right + nombre_embranche_left

                    break

                # Otherwise, the beam continue is travel.

            indice_of_parcours += 1

        return nombre_embranchement
    
    def verify_already_occuped(self, newlist_of_beam : list[Beam], horizontal_position : int):
        """ Verify if the place is not already occupied"""
        boolean_occuped = False
        for beam in newlist_of_beam:
            if beam.horizontal_position == horizontal_position:
                boolean_occuped = True
                break
        return boolean_occuped

def read_file(filename:str, filepath:str):
    """ Read database file given and calculate the result"""

    mytable = Table()

    file_to_read = os.path.join(filepath,filename)
    with open(file_to_read, "r", encoding="utf-8") as fic:
        lines = fic.readlines()
        for line in lines:
            line = line.strip()
            indice = 0
            new_dict = {}
            for string in line:
                new_dict[indice] = string
                indice +=1
            mytable.increment_dict(new_dict)
            
    return mytable

def made_the_calcul(mytable : Table):

    """ Used to make the calc of exercice 7 part 1"""
    
    reponse = mytable.move_forward_in_table()
    print(reponse)

def made_the_calcul_2(mytable : Table):

    """ Used to make the calc of exercice 7 part 1"""
    
    reponse = mytable.move_forward_in_table_quantum()
    print(reponse)

my_table = read_file(filename="input_7.txt", filepath="/home/G5636/Téléchargements")
made_the_calcul_2(mytable=my_table)
