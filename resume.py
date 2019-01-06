import sys

import variable

if (len(sys.argv) != 5):
    raise ValueError('Le nombre de parametre n\'est pas correct. Il faut 4 parametres\n\n'
                     '- Le premier parametre : le nombre de candidats/partis\n'
                     '- le second : le nombre de bureau de votes\n'
                     '- le troisieme : les nombres de personnes votants dans tout le territoire\n'
                     '- le quatrieme : le type de coalition # 0 pour aucune fraude, 1 pour coalition, 2 pour solitaire')

try:
    int(sys.argv[1])
except Exception:
    raise TypeError('Le nombre de Candidats doit etre un entier')

try:
    int(sys.argv[2])
except Exception:
    raise TypeError('Le nombre de Bureaux de vote doit etre un entier')
try:
    int(sys.argv[3])
except Exception:
    raise TypeError('Le nombre de votants doit etre un entier')
try:
    int(sys.argv[4])
except Exception:
    raise TypeError('Le type de coalition doit etre un entier')

if not (int(sys.argv[4]) <= 2 and int(sys.argv[4]) >= 0):
    raise ValueError('Le type de coalition doit etre entre 0 et 2')
variable.PARTIES_LIST = variable.PARTIES_LIST[:int(sys.argv[1])]
variable.BUREAU_VOTES_NUMBER = int(sys.argv[2])
variable.ENROLLED_PEOPLE_NUMBER = int(sys.argv[3])
variable.COALITION_MODE = int(sys.argv[4])
import main
import PdfToImage
import OCR
