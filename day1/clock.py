""" Exercice 1 of adventofcode"""

import os

class Clock : 

    """ Horloge """

    def __init__(self):
        self.occurency = 0
        self.occurency_one = 0
        self.actual_case = 50
        self.number_of_rotate = 0

    def rotate(self, direction:str, number:int):
        """ Rotation class part, in addition compt every occurence of 0 """

        self.number_of_rotate = self.number_of_rotate + 1

        if direction == "R":
            # Using modulo and adding because of turning right
            number_of_return_to_0 = ( self.actual_case + number ) // 100
            self.actual_case = ( self.actual_case + number ) % 100
            print(f"adding {number} ... Moving to this score : {self.actual_case}")
        elif direction == "L":
            # Using modulo and substracting because of turning left
            flipped_arrow = (100-self.actual_case)%100
            number_of_return_to_0 = (flipped_arrow + number)//100
            self.actual_case = ( self.actual_case - number ) % 100
            print(f"substracting {number} ... Moving to this score : {self.actual_case}")
        else:
            number_of_return_to_0 = 0
            print("Not respectful of my work")

        if number_of_return_to_0 != 0:
            # If rotation is on 0, occurence add to be add
            print(f"adding {number_of_return_to_0} to the occurence")
            self.occurency += number_of_return_to_0
            print(f"Actual number of occurence : {self.occurency}")
        if self.actual_case == 0:
            self.occurency_one += 1
    def read_file(self, filename:str, filepath:str):
        """ Read database file given and calculate the result"""

        file_to_read = os.path.join(filepath,filename)
        with open(file_to_read, "r", encoding="utf-8") as fic:
            lines = fic.readlines()
            for line in lines:
                self.rotate(direction = line[0], number = int(line[1:]))
        print(f"Final result is (1): {self.occurency_one}")
        print(f"Final result is (2): {self.occurency}")
        print(f"Number of rotation : {self.number_of_rotate}")

clock = Clock()
clock.read_file(filename="input.txt", filepath="/home/G5636/Téléchargements")
