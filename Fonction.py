import random
import variable

from PV import PV
#from variable import PARTIES_LIST


class Fonction:
    def generateRandomNumbers(cls, number_of_numbers_to_generate, main_number):
        top = main_number + number_of_numbers_to_generate - 1
        temp = []
        if number_of_numbers_to_generate == 1:
            real_number = []
            real_number.append(main_number)
            return real_number
        for i in range(number_of_numbers_to_generate - 1):
            var = random.randint(1, top)
            while var in temp:
                var = random.randint(1, top)
            temp.append(var)

        temp.sort()
        real_number = []
        for i in range(number_of_numbers_to_generate - 1):
            if i == 0:
                real_number.append(temp[0] - 1)
            else:
                real_number.append(temp[i] - temp[i - 1] - 1)
        if temp is not []:
            real_number.append(top - temp[-1])
        else:
            real_number.append(main_number)

        return real_number

    generateRandomNumbers = classmethod(generateRandomNumbers)

    def generateRandomNumbersWithPref(cls, number_of_numbers_to_generate, main_number, id_to_win):
        var = Fonction.generateRandomNumbers(number_of_numbers_to_generate, main_number)
        while var[id_to_win] != max(var):
            var = Fonction.generateRandomNumbers(number_of_numbers_to_generate, main_number)
        return var

    generateRandomNumbersWithPref = classmethod(generateRandomNumbersWithPref)

    def generatePVForBureauWithCoalitionMode(cls, real_result, coalition_mode, party_to_favorite='',
                                             coalition_group=[]):
        pv_list = []
        if coalition_mode == 0:
            print("Le bon résultat" + str(real_result))
            for index, item in enumerate(real_result):
                pv = PV(variable.PARTIES_LIST[index])
                pv.party_results = real_result
                pv_list.append(pv)
            return pv_list
        elif coalition_mode == 1:
            generate_pv = Fonction.generateRandomNumbersWithPref(len(variable.PARTIES_LIST), sum(real_result), party_to_favorite)
            for index, item in enumerate(real_result):
                pv = PV(variable.PARTIES_LIST[index])
                if index in coalition_group:
                    # pv.party_results = [(PARTIES_LIST[i], votes) for i, votes in
                    #                     enumerate(generatePV)]
                    pv.party_results = [votes for votes in
                                        generate_pv]
                else:
                    pv.party_results = real_result
                pv_list.append(pv)
            return pv_list
        else:
            for index, item in enumerate(real_result):
                pv = PV(variable.PARTIES_LIST[index])
                pv.party_results = Fonction.generateRandomNumbersWithPref(len(real_result), sum(real_result),
                                                                          index)
                pv_list.append(pv)
            return pv_list

    generatePVForBureauWithCoalitionMode = classmethod(generatePVForBureauWithCoalitionMode)

    def generateTabRandomElementsDiff(cls, number_of_items, totals_elements):
        list_t = []
        while len(list_t) != number_of_items:
            var = random.randint(0, totals_elements - 1)
            if var not in list_t:
                list_t.append(var)
        return list_t

    generateTabRandomElementsDiff = classmethod(generateTabRandomElementsDiff)
