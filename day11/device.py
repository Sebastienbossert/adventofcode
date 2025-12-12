import os

class Device  :

    """ Define a Device """

    def __init__(self, name_of_device : str, passed_on_dac : bool, passed_on_fft: bool):

        """ Init function """

        self.name_of_device = name_of_device
        self.passed_on_dac = passed_on_dac
        self.passed_on_fft = passed_on_fft

    def soulking(self, passed_on_dac : bool, passed_on_fft: bool):
        """ Made true if true, or no change :) """

        parameter1 = False
        parameter2 = False

        if not self.passed_on_dac and self.passed_on_fft:
            if passed_on_fft:
                parameter1 = passed_on_dac

        if not self.passed_on_fft and self.passed_on_dac:
            if passed_on_dac:
                parameter2 = passed_on_fft

        if self.passed_on_fft and self.passed_on_dac:
            parameter1 = True
            parameter2 = True

        if passed_on_dac and passed_on_fft:
            parameter1 = True
            parameter2 = True           
        
        return (parameter1 and parameter2)
            

class Calc :

    def __init__(self):

        """ Init function """

        self.compteur_total = 0

    def recursive_made(self, list_to_check : list[dict|str]):
            
        for list_of_imbracated_list in list_to_check :
            if "out" == list_of_imbracated_list:
                self.compteur_total += 1
            elif isinstance(list_of_imbracated_list,list):
                self.recursive_made(list_to_check=list_of_imbracated_list)
            else:
                self.recursive_made(list_to_check=list_of_imbracated_list.values())
        
        return self.compteur_total
    
class Link :
    def __init__(self, name_of_device : str):

        """ Init function """

        self.name_of_device = name_of_device
        self.list_of_device_name = []
        self.passed_on_dac = False
        self.passed_on_fft = False
    
class Calc2 :

    def __init__(self):

        """ Init function """

        self.compteur_total = 0
        self.already_passed : [Device] = []
        self.global_dict = {}

    def chope_moi_lecollback(self):

        """ On calcul en local pour pas de mauvaise surprise """

        link_to_check = self.global_dict["svr"]
        compteur_total = self.recursive_made_2(newlink=link_to_check)

        return compteur_total
    
    def build_dict(self, lines):
        """ Build dict to conserv reference between member """
        
        for line in lines:

            line = line.strip()
            position = line.split(":")
            
            dict_name=position[0]
            self.global_dict[dict_name] = Link(dict_name)

        for line in lines:

            line = line.strip()
            position = line.split(":")
            
            temporary = position[1].strip()
            temporary = temporary.split(" ")
            dict_name_link = position[0]

            for temp in temporary:
                if temp == "out":
                    self.global_dict[dict_name_link].list_of_device_name.append("out")
                elif temp in self.global_dict.keys() and dict_name_link in self.global_dict.keys():
                    # We made junction enter dict
                    self.global_dict[dict_name_link].list_of_device_name.append(Link(name_of_device=temp))
                else:
                    print("Weird stuff happened")

    def recursive_made_2(self, newlink : Link):

        list_to_check = []

        for name_of_device in newlink.list_of_device_name:
            if name_of_device == "out":
                list_to_check.append("out")
            else: 
                list_to_check.append(self.global_dict[name_of_device.name_of_device])

        list_to_check_copy = list_to_check.copy()
        for list_of_imbracated_list in list_to_check :

            if list_of_imbracated_list != "out":
                
                result_already_passed = False
                for device_name in self.already_passed:

                    if list_of_imbracated_list.name_of_device == device_name:

                        newlink.passed_on_fft = list_of_imbracated_list.passed_on_fft if list_of_imbracated_list.passed_on_fft else newlink.passed_on_fft
                        newlink.passed_on_dac = list_of_imbracated_list.passed_on_dac if list_of_imbracated_list.passed_on_dac else newlink.passed_on_dac
                        result_already_passed = True

                        list_to_check_copy.remove(list_of_imbracated_list)

                if "fft" == newlink.name_of_device:
                    
                    newlink.passed_on_fft = True
                    list_of_imbracated_list.passed_on_fft = True

                if "dac" == newlink.name_of_device:

                    newlink.passed_on_dac = True
                    list_of_imbracated_list.passed_on_dac = True

                if not result_already_passed:

                    self.already_passed.append(list_of_imbracated_list.device_name)
                    oldlink = newlink
                    self.recursive_made_2(newlink=list_of_imbracated_list)
                    oldlink.passed_on_dac = list_of_imbracated_list.passed_on_dac if list_of_imbracated_list.passed_on_dac else oldlink.passed_on_dac
                    oldlink.passed_on_fft = list_of_imbracated_list.passed_on_fft if list_of_imbracated_list.passed_on_fft else oldlink.passed_on_fft
                    if oldlink.passed_on_dac and oldlink.passed_on_fft:
                        self.compteur_total += 1

            else:

                list_to_check_copy.remove(list_of_imbracated_list)
        
        for link in newlink.list_of_device_name :
            if link != "out":
                oldlink = newlink
                self.recursive_made_2(newlink=link)
                oldlink.passed_on_dac = link.passed_on_dac if link.passed_on_dac else oldlink.passed_on_dac
                oldlink.passed_on_fft = link.passed_on_fft if link.passed_on_fft else oldlink.passed_on_fft

        return self.compteur_total

    def recursive_made(self, newlink : Link, occur_name : str = "", exclude_infinite_loop : list = []):
        
        list_to_check = []

        for name_of_device in newlink.list_of_device_name:
            if not isinstance(name_of_device,list) and not isinstance(name_of_device, Device):
                list_to_check.append(self.global_dict[name_of_device])
            
        for list_of_imbracated_list in list_to_check :

            if "fft" == newlink.name_of_device:
                
                newlink.passed_on_fft = True
                list_of_imbracated_list.passed_on_fft = True

            if "dac" == newlink.name_of_device:

                newlink.passed_on_dac = True
                list_of_imbracated_list.passed_on_dac = True

            already_passed = False
            is_something_to_count = False

            temp_key = ""

            for device in self.already_passed:
                if isinstance(list_of_imbracated_list, Link):
                    for link in list_of_imbracated_list.list_of_device_name:
                        if link != "out":
                            temp_key = link
                            if temp_key == device.name_of_device:
                                already_passed = True
                                is_something_to_count = device.soulking(passed_on_fft=newlink.passed_on_fft, passed_on_dac=newlink.passed_on_dac)
                                if is_something_to_count:
                                    self.compteur_total +=1
                elif isinstance(list_of_imbracated_list, list):
                    for device2 in list_of_imbracated_list:
                        if device2.name_of_device != "out":
                            temp_key = device2.name_of_device
                            if temp_key == device.name_of_device:
                                already_passed = True
                                is_something_to_count = device2.soulking(passed_on_fft=device.passed_on_fft, passed_on_dac=device.passed_on_dac)
                                if is_something_to_count:
                                    self.compteur_total +=1
                                else:
                                    device2.passed_on_fft = device.passed_on_fft if device.passed_on_fft else device2.passed_on_fft
                                    device2.passed_on_dac = device.passed_on_dac if device.passed_on_dac else device2.passed_on_dac


            if not already_passed:

                list_to_check_2 = []
        
                for name_of_device in list_of_imbracated_list.list_of_device_name:

                    if isinstance(name_of_device, Device):
                        list_to_check_2.append(self.global_dict[name_of_device.name_of_device])
                    elif name_of_device != "out":
                        list_to_check_2.append(self.global_dict[name_of_device])
                    else:
                        list_to_check_2.append("out")
                
                for value in list_to_check_2:

                    if isinstance(value,Device):

                        is_something_to_count = list_of_imbracated_list.soulking(passed_on_fft=value.passed_on_fft, passed_on_dac=value.passed_on_dac)

                        if is_something_to_count:

                            self.compteur_total += 1


                    if value != "out" :

                        if value.name_of_device not in exclude_infinite_loop:

                            exclude_infinite_loop_new = exclude_infinite_loop.copy()
                            exclude_infinite_loop.append(value.name_of_device)
                            value.passed_on_dac = list_of_imbracated_list.passed_on_dac if list_of_imbracated_list.passed_on_dac else value.passed_on_dac
                            value.passed_on_fft = list_of_imbracated_list.passed_on_fft if list_of_imbracated_list.passed_on_fft else value.passed_on_fft
                            self.recursive_made(newlink=value, occur_name=value.name_of_device, exclude_infinite_loop=exclude_infinite_loop_new)

                        else:

                            new_device = Device(name_of_device=list_of_imbracated_list.name_of_device, passed_on_dac=list_of_imbracated_list.passed_on_dac, passed_on_fft=list_of_imbracated_list.passed_on_fft)
                            self.already_passed.append(new_device)
                            
                            print(f"Mongolise {occur_name}")
                        
                    else:

                        new_device = Device(name_of_device=list_of_imbracated_list.name_of_device,passed_on_dac=list_of_imbracated_list.passed_on_dac,passed_on_fft=list_of_imbracated_list.passed_on_fft)
                        self.already_passed.append(new_device)
                        
                        self.global_dict[list_of_imbracated_list.name_of_device].list_of_device_name.remove(value)
                        self.global_dict[list_of_imbracated_list.name_of_device].list_of_device_name.append(new_device)

                if list_of_imbracated_list.list_of_device_name:
                    only_device = True
                    for value in list_of_imbracated_list.list_of_device_name:
                        if not isinstance(value, Device):
                            only_device = False
                    if only_device:
                        for device in list_of_imbracated_list.list_of_device_name:
                            is_something_to_count = device.soulking(passed_on_fft=list_of_imbracated_list.passed_on_fft, passed_on_dac=list_of_imbracated_list.passed_on_dac)
                            if is_something_to_count:
                                self.compteur_total += 1
                            else:
                                list_of_imbracated_list.passed_on_fft = device.passed_on_fft if device.passed_on_fft else list_of_imbracated_list.passed_on_fft
                                list_of_imbracated_list.passed_on_dac = device.passed_on_dac if device.passed_on_dac else list_of_imbracated_list.passed_on_dac
                            self.global_dict[list_of_imbracated_list.name_of_device] = list_of_imbracated_list
        
        return self.compteur_total

def made_the_calc_part_1(dict_of_device : dict):
    """ Made the calc of part 1"""

    list_to_check = dict_of_device["you"]
    calc = Calc()
    compteur_total = calc.recursive_made(list_to_check=list_to_check)
    print(compteur_total)

def made_the_calc_part_2(calc2 : Calc2):
    """ Made the calc of part 1"""

    compteur_total = calc2.chope_moi_lecollback()
    print(compteur_total)

def read_file(filename:str, filepath:str):
    """ Read database file given and calculate the result"""

    dict_of_device : dict[str] = {}
    
    file_to_read = os.path.join(filepath,filename)

    with open(file_to_read, "r", encoding="utf-8") as fic:

        calc = Calc2()
        
        lines = fic.readlines()
        calc.build_dict(lines)

        for line in lines:

            line = line.strip()
            position = line.split(":")
            
            dict_name=position[0]
            dict_of_device[dict_name] = []

        for line in lines:

            line = line.strip()
            position = line.split(":")
            
            temporary = position[1].strip()
            temporary = temporary.split(" ")
            dict_name_link = position[0]

            for temp in temporary:
                if temp == "out":
                    dict_of_device[dict_name_link].append("out")
                elif temp in dict_of_device.keys() and dict_name_link in dict_of_device.keys():
                    # We made junction enter dict
                    dict_of_device[dict_name_link].append({temp:dict_of_device[temp]})
                else:
                    print("Weird stuff happened")

    return dict_of_device, calc

dict_of_device, calc2 = read_file(filename="input_11_2_exemple.txt", filepath="/home/G5636/Téléchargements")    
made_the_calc_part_2(calc2)
