# Ici, je vais mettre toutes les configurations dont j'ai besoin pour effectuer le traitement demande


PARTIES_LIST = ['RDPC', 'MRC', 'SDF', 'FPD', 'ADD', 'UDC', 'UNIVERS', 'PURS', 'MCNC', 'ANDP', 'CPP', 'SCNC', 'MP']
BUREAU_VOTES_NUMBER = 10
ENROLLED_PEOPLE_NUMBER = 15000
COALITION_MODE = 1  # 0 pour aucune fraude, 1 pour coalition, 2 pour solitaire


def getCoalitionName(coalition_mode):
    if coalition_mode == 0:
        return "Aucune Fraude"
    elif coalition_mode == 1:
        return "Coalition simple"
    else:
        return "Totale Coalition"
