""" Exercice 2 of adventofcode"""

import os

class Product :

    """ Gift shop """

    def __init__(self, lastid:str, firstid: str):
        self.last_id = lastid
        self.first_id = firstid

    def found_invalid_id_part_1(self) -> list:
        """ Method used to determine what is an invalid id (can be more than one), for part one"""

        invalid_id_list = []
        range_depart = int(self.first_id)

        while range_depart <= int(self.last_id):
            range_depart_str = str(range_depart)
            range_depart_str_len = int(len(range_depart_str) / 2)
            if range_depart_str[0:range_depart_str_len] == range_depart_str[range_depart_str_len:]:
                invalid_id_list.append(range_depart)
            range_depart += 1

        return invalid_id_list

    def found_invalid_id_part_2(self) -> list:
        """ Method used to determine what is an invalid id (can be more than one), for part two"""

        invalid_id_list = []
        range_depart = int(self.first_id)

        while range_depart <= int(self.last_id):

            range_depart_str = str(range_depart)
            range_depart_str_len_divide = int(len(range_depart_str) / 2)
            range_depart_str_len = int(len(range_depart_str))

            # There is the move for the part2. Obviously we have to view all case possible
            init_int = 1
            while init_int <= range_depart_str_len_divide:
                list_segmentate = []
                # Loop through the string and split it into segments
                for i in range(0, range_depart_str_len, init_int):
                    segment = range_depart_str[i:i + init_int]  # slice the string
                    list_segmentate.append(segment)  # add the segment to the list
                first_segment = list_segmentate[0]
                take_in_accompt = True
                for segmentation in list_segmentate :
                    if segmentation != first_segment:
                        take_in_accompt = False
                if take_in_accompt:
                    invalid_id_list.append(range_depart)
                    break
                init_int += 1

            range_depart += 1

        return invalid_id_list


def read_file(filename:str, filepath:str):
    """ Read database file given and calculate the result"""

    table_of_product = []

    file_to_read = os.path.join(filepath,filename)
    with open(file_to_read, "r", encoding="utf-8") as fic:
        lines = fic.readlines()
        for line in lines:
            table_of_occurency = line.split(",")
            for occurency in table_of_occurency:
                table_split_id = occurency.split("-")
                new_product = Product(table_split_id[1], table_split_id[0])
                table_of_product.append(new_product)

    return table_of_product

def made_the_calcul_part_1(products:list):
    """ Used to made the calc of part 1 of exercice 2"""
    int_final = 0
    for product in products:
        list_of_invalid_id = product.found_invalid_id_part_1()
        for invalid_id in list_of_invalid_id:
            int_final += invalid_id
    print(int_final)

def made_the_calcul_part_2(products:list):
    """ Used to made the calc of part 1 of exercice 2"""
    int_final = 0
    for product in products:
        list_of_invalid_id = product.found_invalid_id_part_2()
        for invalid_id in list_of_invalid_id:
            int_final += invalid_id
    print(int_final)


table_of_all_product = read_file(filename="input_2.txt", filepath="/home/G5636/Téléchargements")
made_the_calcul_part_1(table_of_all_product)
made_the_calcul_part_2(table_of_all_product)
