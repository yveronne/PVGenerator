import random

from PV import PV
from variable import BUREAU_VOTES_NUMBER, ENROLLED_PEOPLE_NUMBER, PARTIES_LIST, COALITION_MODE, getCoalitionName

from BureauVote import BureauVote
from Fonction import Fonction

bureauVotes_List, results = [], []
repartitions = Fonction.generateRandomNumbers(BUREAU_VOTES_NUMBER, ENROLLED_PEOPLE_NUMBER)

# je dispatche les nombres d'inscrits entre les bureaux de vote
for i in range(BUREAU_VOTES_NUMBER):
    bureauVotes_List.append(BureauVote('Bureau_de_Vote_' + str(i + 1), repartitions[i]))

# j'enregistre les resultats reels de chaque parti dans chaque bureau de vote, (RDPC,nbreVotes)
for bureau in bureauVotes_List:
    pv = PV("Reference")
    pv.party_results = Fonction.generateRandomNumbers(len(PARTIES_LIST), bureau.enrolled_persons)
    bureau.results = pv
    # bureau.results = [(PARTIES_LIST[i], votes) for i, votes in
    #                   enumerate(Fonction.generateRandomNumbers(len(PARTIES_LIST), bureau.enrolled_persons))]

# c'est la partie ou on commence a generer les pv en fonction de la fraude

# print(Fonction.generatePVForBureauWithCoalitionMode(bureauVotes_List[0].results, COALITION_MODE, 2, [0, 6, 2]))
# Ici on genere tous les PV avec une eventuelle coalition
number_of_coalised_party = random.randint(1, len(PARTIES_LIST) - 1)
coalised_group = Fonction.generateTabRandomElementsDiff(number_of_coalised_party, len(PARTIES_LIST))
party_favorite = random.choice(coalised_group)
print('il ya coalition ' + str(COALITION_MODE))
print('le groupe qui fait la coalition est :' + str(coalised_group))
print('le party choisi est :' + str(party_favorite))

for bureau in bureauVotes_List:
    bureau.all_pv = Fonction.generatePVForBureauWithCoalitionMode(bureau.results.party_results, COALITION_MODE,
                                                                  party_favorite,
                                                                  coalised_group)

for bureau in bureauVotes_List:
    t = random.choices([0, 1], [0.35, 0.65])[0]
    if t:
        pv = PV("Elecam")
        pv.party_results = Fonction.generateRandomNumbersWithPref(len(PARTIES_LIST), bureau.enrolled_persons, 0)
        bureau.elecam_pv = pv
    else:
        pv = PV("Elecam")
        pv.party_results = bureau.results.party_results
        bureau.elecam_pv = pv
for bureau in bureauVotes_List:
    print(bureau)
    for item in bureau.all_pv:
        print(item)

# Creation de tous les dossiers

import os

for party in PARTIES_LIST:
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'PV_PDF', party)):
        os.makedirs(os.path.join(os.path.dirname(__file__), 'PV_PDF', party))

if not os.path.exists(os.path.join(os.path.dirname(__file__), 'PV_PDF', 'REAL_RESULT')):
    os.makedirs(os.path.join(os.path.dirname(__file__), 'PV_PDF', 'REAL_RESULT'))

if not os.path.exists(os.path.join(os.path.dirname(__file__), 'PV_PDF', 'ELECAM')):
    os.makedirs(os.path.join(os.path.dirname(__file__), 'PV_PDF', 'ELECAM'))

# Generating PDF files
from fpdf import FPDF

width_cell, height_cell = 150, 40

for bureau in bureauVotes_List:
    for PV in bureau.all_pv:
        pdf = FPDF(orientation='P', unit='pt', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", size=16)
        pdf.multi_cell(0, 20, "PV_" + bureau.name, 0)
        pdf.set_top_margin(20)
        pdf.set_font("Arial", size=14)
        pdf.multi_cell(0, 20, "Nombre_de_Votants : " + str(bureau.enrolled_persons), 0)
        pdf.set_top_margin(20)
        pdf.multi_cell(0, 20, "Type_de_Coalition : " + str(getCoalitionName(COALITION_MODE)), 0)
        pdf.set_top_margin(20)
        pdf.set_fill_color(193, 229, 252)
        pdf.cell(width_cell, height_cell, 'Nom_du_Parti', 1, 0, 'C', 1)
        pdf.cell(width_cell, height_cell, 'Nombre_de_Voix', 1, 1, 'C', 1)
        for index, votes in enumerate(PV.party_results):
            pdf.set_font("Arial", size=14)
            pdf.cell(width_cell, height_cell, str(PARTIES_LIST[index]), 1, 0, 'L', 0)
            pdf.set_font("Arial", size=14)
            pdf.cell(width_cell, height_cell, str(votes), 1, 1, 'L', 0)
        pdf.set_font("Arial", size=14)
        pdf.multi_cell(0, 20, "", 0)
        pdf.set_top_margin(20)
        pdf.set_fill_color(193, 229, 252)
        pdf.cell(width_cell, height_cell, 'Nom_du_Representant', 1, 0, 'C', 1)
        pdf.cell(2 * width_cell, height_cell, 'Signatures', 1, 1, 'C', 1)
        for index, votes in enumerate(PV.party_results):
            pdf.set_font("Arial", size=14)
            pdf.cell(width_cell, height_cell, str(PARTIES_LIST[index]), 1, 0, 'L', 0)
            pdf.set_font("Arial", size=12)
            pdf.cell(2 * width_cell, height_cell,
                     "Scrutateur_" + str(PARTIES_LIST[index]) + "_" + str(bureau.name), 1, 1, 'L', 0)

        pdf.output('PV_PDF/' + str(PV.party_name) + '/PV_' + str(bureau.name) + '.pdf')

    # pour mettre les PV d'elecam
    pdf = FPDF(orientation='P', unit='pt', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.multi_cell(0, 20, "PV_ELECAM_" + bureau.name, 0)
    pdf.set_top_margin(20)
    pdf.set_font("Arial", size=14)
    pdf.multi_cell(0, 20, "Nombre_de_Votants : " + str(bureau.enrolled_persons), 0)
    pdf.set_top_margin(20)
    pdf.multi_cell(0, 20, "Type_de_Coalition : " + str(getCoalitionName(COALITION_MODE)), 0)
    pdf.set_top_margin(20)
    pdf.set_fill_color(193, 229, 252)
    pdf.cell(width_cell, height_cell, 'Nom_du_Parti', 1, 0, 'C', 1)
    pdf.cell(width_cell, height_cell, 'Nombre_de_Voix', 1, 1, 'C', 1)
    for index, votes in enumerate(bureau.elecam_pv.party_results):
        pdf.set_font("Arial", size=14)
        pdf.cell(width_cell, height_cell, str(PARTIES_LIST[index]), 1, 0, 'L', 0)
        pdf.set_font("Arial", size=14)
        pdf.cell(width_cell, height_cell, str(votes), 1, 1, 'L', 0)
    pdf.set_font("Arial", size=14)
    pdf.multi_cell(0, 20, "", 0)
    pdf.set_top_margin(20)
    pdf.set_fill_color(193, 229, 252)
    pdf.cell(width_cell, height_cell, 'Nom_du_Representant', 1, 0, 'C', 1)
    pdf.cell(2 * width_cell, height_cell, 'Signatures', 1, 1, 'C', 1)
    for index, votes in enumerate(bureau.elecam_pv.party_results):
        pdf.set_font("Arial", size=14)
        pdf.cell(width_cell, height_cell, str(PARTIES_LIST[index]), 1, 0, 'L', 0)
        pdf.set_font("Arial", size=12)
        pdf.cell(2 * width_cell, height_cell,
                 "Scrutateur_" + str(PARTIES_LIST[index]) + "_" + str(bureau.name), 1, 1, 'L', 0)

    pdf.output('PV_PDF/ELECAM/PV_Elecam_' + str(bureau.name) + '.pdf')

    # pour mettre les PV de reference
    pdf = FPDF(orientation='P', unit='pt', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.multi_cell(0, 20, "PV_GAGNANT_" + bureau.name, 0)
    pdf.set_top_margin(20)
    pdf.set_font("Arial", size=14)
    pdf.multi_cell(0, 20, "Nombre_de_Votants : " + str(bureau.enrolled_persons), 0)
    pdf.set_top_margin(20)
    pdf.multi_cell(0, 20, "Type_de_Coalition : " + str(getCoalitionName(COALITION_MODE)), 0)
    pdf.set_top_margin(20)
    pdf.set_fill_color(193, 229, 252)
    pdf.cell(width_cell, height_cell, 'Nom_du_Parti', 1, 0, 'C', 1)
    pdf.cell(width_cell, height_cell, 'Nombre_de_Voix', 1, 1, 'C', 1)
    for index, votes in enumerate(bureau.results.party_results):
        pdf.set_font("Arial", size=14)
        pdf.cell(width_cell, height_cell, str(PARTIES_LIST[index]), 1, 0, 'L', 0)
        pdf.set_font("Arial", size=14)
        pdf.cell(width_cell, height_cell, str(votes), 1, 1, 'L', 0)
    pdf.set_font("Arial", size=14)
    pdf.multi_cell(0, 20, "", 0)
    pdf.set_top_margin(20)
    pdf.set_fill_color(193, 229, 252)
    pdf.cell(width_cell, height_cell, 'Nom_du_Representant', 1, 0, 'C', 1)
    pdf.cell(2 * width_cell, height_cell, 'Signatures', 1, 1, 'C', 1)
    for index, votes in enumerate(bureau.results.party_results):
        pdf.set_font("Arial", size=14)
        pdf.cell(width_cell, height_cell, str(PARTIES_LIST[index]), 1, 0, 'L', 0)
        pdf.set_font("Arial", size=12)
        pdf.cell(2 * width_cell, height_cell,
                 "Scrutateur_" + str(PARTIES_LIST[index]) + "_" + str(bureau.name), 1, 1, 'L', 0)

    pdf.output('PV_PDF/REAL_RESULT/PV_Gagnant_' + str(bureau.name) + '.pdf')
