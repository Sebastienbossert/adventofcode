import os
import math
from shapely.geometry import Polygon, box
from shapely.prepared import prep

class Point :
    """ Define a Box """

    def __init__(self, x_position : int, y_position: int):

        """ Init function """
        self.x_position = x_position
        self.y_position = y_position

class Rectangle :
    """ Define all rectangles made of points """

    def __init__(self, list_of_point : list[Point]) :
        """ Init function """
        self.dict_of_rectangle_value = {}
        self.dict_of_rectangle_value_limited = {}
        self.list_of_green_point = []
        self.list_of_point = list_of_point

    def determine_max_rectangle(self, point1: Point, point2: Point):
        """ Used to calculate area of rectangle """

        # Calculate length and width
        length = abs(point2.x_position - point1.x_position) + 1
        width = abs(point2.y_position - point1.y_position) + 1

        # Calculate area
        area = length * width
        
        return area

    
    def build_dict_of_area(self):

        """ Used to make the dict of all distances """
        indice = 0

        for point1 in self.list_of_point:

            indice += 1

            # Point 1 perspective

            if point1 not in self.dict_of_rectangle_value:
                self.dict_of_rectangle_value[point1] = {}

            actual_chiffre = indice

            # Point 2 perspective

            while actual_chiffre < len(self.list_of_point):
                self.dict_of_rectangle_value[point1][self.list_of_point[actual_chiffre]] = self.determine_max_rectangle(point1, self.list_of_point[actual_chiffre])
                actual_chiffre += 1

    def determinate_max_area(self):

        """ Used to answer the max area rectangle from the list """
        max_area = 0
        for _, value in self.dict_of_rectangle_value.items():
            for _, valuefinal in value.items():
                if max_area < valuefinal:
                    max_area = valuefinal
        
        return max_area
    
    def make_list_of_green_point(self):

        """ Used to make the list of position of green point """

        list_of_green_point : list [Point] = self.list_of_point.copy()
        old_point = None

        for point1 in self.list_of_point:

            if not old_point:

                old_point = point1

            else:

                if point1.x_position == old_point.x_position:
                    y_axes = point1.y_position
                    y_axes_to_reach = old_point.y_position
                    if y_axes_to_reach < y_axes:
                        temp = y_axes
                        y_axes = y_axes_to_reach
                        y_axes_to_reach = temp
                    while y_axes < y_axes_to_reach:
                        list_of_green_point.append(Point(x_position=point1.x_position, y_position=y_axes))
                        y_axes +=1
                else:
                    x_axes = point1.x_position
                    x_axes_to_reach = old_point.x_position
                    if x_axes_to_reach < x_axes:
                        temp = x_axes
                        x_axes = x_axes_to_reach
                        x_axes_to_reach = temp
                    while x_axes < x_axes_to_reach:
                        list_of_green_point.append(Point(x_position=x_axes, y_position=point1.y_position))
                        x_axes += 1
            
        self.list_of_green_point = list_of_green_point

    def determine_max_rectangle_with_limited(self):

        """ Determine the max area reactangle with limited size"""

        if not self.list_of_green_point:
            self.make_list_of_green_point()

        tuple_mapping = [(point.x_position,point.y_position) for point in self.list_of_point]
        polygon = Polygon(tuple_mapping)
        prepared_polygon = prep(polygon)

        max_area = 0
        indice = 0

        for point1 in self.list_of_point:

            indice += 1

            # Point 1 perspective

            if point1 not in self.dict_of_rectangle_value:
                self.dict_of_rectangle_value[point1] = {}

            actual_chiffre = indice

            # Point 2 perspective

            while actual_chiffre < len(self.list_of_point):

                point2 = self.list_of_point[actual_chiffre]
                
                area = self.determine_max_rectangle(point1, point2)
                if area <= max_area:
                    actual_chiffre+=1
                    continue

                other_ectangle = box(
                    min(point1.x_position, point2.x_position), min(point1.y_position, point2.y_position), max(point1.x_position, point2.x_position), max(point1.y_position, point2.y_position)
                )

                if prepared_polygon.contains(other_ectangle):
                    if max_area < area :
                        max_area = area
                
                actual_chiffre+=1

        return max_area



    def build_dict_of_area_exercice2(self):
        """ Used to make the dict of all distances """
        indice = 0

        for point1 in self.list_of_point:

            indice += 1

            # Point 1 perspective

            if point1 not in self.dict_of_rectangle_value:
                self.dict_of_rectangle_value_limited[point1] = {}

            actual_chiffre = indice

            # Point 2 perspective

            while actual_chiffre < len(self.list_of_point):
                self.dict_of_rectangle_value_limited[point1][self.list_of_point[actual_chiffre]] = self.determine_max_rectangle(point1, self.list_of_point[actual_chiffre])
                actual_chiffre += 1

def read_file(filename:str, filepath:str):
    """ Read database file given and calculate the result"""

    list_of_point : list[Point]= []

    file_to_read = os.path.join(filepath,filename)
    with open(file_to_read, "r", encoding="utf-8") as fic:
        lines = fic.readlines()
        for line in lines:
            line = line.strip()
            position = line.split(",")
            new_point = Point(x_position=int(position[0]), y_position=int(position[1]))
            list_of_point.append(new_point)

    new_rectangle = Rectangle(list_of_point=list_of_point)
            
    return new_rectangle

def made_the_calcul(rectangle : Rectangle):
    """ Used to make the calc of exercice 9 part 1"""
    rectangle.build_dict_of_area()
    retour = rectangle.determinate_max_area()
    print(retour)

def made_the_calcul_2(rectangle : Rectangle):
    """ Used to make the calc of exercice 9 part 2"""
    retour = rectangle.determine_max_rectangle_with_limited()
    print(retour)

rectangle = read_file(filename="input_9.txt", filepath="/home/G5636/Téléchargements")
made_the_calcul_2(rectangle=rectangle)
