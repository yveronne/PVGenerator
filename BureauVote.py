from PV import PV


class BureauVote:
    def __init__(self, name, enrolled_persons):
        self.name = name
        self.enrolled_persons = enrolled_persons
        self.results = PV()
        '''ce sont les vrais resultats du bureau de vote. c'est la reference. c'est sous la forme (nomParti,voix)'''
        self.all_pv = []
        self.elecam_pv = PV()

    def __str__(self):
        return "Le " + str(self.name) + " a " + str(self.enrolled_persons) + " personnes inscrites" + str(
            self.results) + " " + str(self.elecam_pv)

    def addPV(self, pv):
        self.all_pv.append(pv)
