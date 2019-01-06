class PV:
    def __init__(self, party_name=''):
        self.party_name = party_name
        self.party_results = []
        '''ce sont les vrais resultats du bureau de vote. c'est la reference. c'est sous la forme (nomParti,voix)'''

    def __str__(self):
        return "Le "+str(self.party_name)+" a "+str(self.party_results)+" personnes inscrites"