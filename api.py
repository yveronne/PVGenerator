import os
import variable

from flask import Flask, request
from flask_api import status

app = Flask(__name__)


@app.route('/api', methods=['POST'])
def index():
    try:
        tab = ['RDPC', 'MRC', 'SDF', 'FPD', 'ADD', 'UDC', 'UNIVERS', 'PURS', 'MCNC', 'ANDP', 'CPP', 'SCNC', 'MP']
        variable.PARTIES_LIST = tab[:int(request.args.get('number_party'))]
        print("Je récupère les partis ")
        print(variable.PARTIES_LIST)
        variable.BUREAU_VOTES_NUMBER = int(request.args.get('bureau_number'))
        variable.ENROLLED_PEOPLE_NUMBER = int(request.args.get('enrolled_number'))
        variable.COALITION_MODE = int(request.args.get('coalition_mode'))
    except Exception:
        return str(status.HTTP_400_BAD_REQUEST), "The data is not in the real format"
    try:
        import shutil
        if os.path.exists(os.path.join(os.path.dirname(__file__), 'PV_IMAGE')):
            shutil.rmtree(os.path.join(os.path.dirname(__file__), 'PV_IMAGE'))
            os.makedirs(os.path.join(os.path.dirname(__file__), 'PV_IMAGE'))
        if os.path.exists(os.path.join(os.path.dirname(__file__), 'PV_PDF')):
            shutil.rmtree(os.path.join(os.path.dirname(__file__), 'PV_PDF'))
            os.makedirs(os.path.join(os.path.dirname(__file__), 'PV_PDF'))

        

        import random

        from PV import PV
        from variable import BUREAU_VOTES_NUMBER, ENROLLED_PEOPLE_NUMBER, PARTIES_LIST, COALITION_MODE, getCoalitionName

        from BureauVote import BureauVote
        from Fonction import Fonction

        bureauVotes_List = []
        print(PARTIES_LIST)
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
        for bureau in bureauVotes_List:
            bureau.all_pv = Fonction.generatePVForBureauWithCoalitionMode(bureau.results.party_results, COALITION_MODE, party_favorite, coalised_group)
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

        #import os

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




        #import os
        from pdf2jpg import pdf2jpg

        from variable import PARTIES_LIST

        #import shutil
        if os.path.exists(os.path.join(os.path.dirname(__file__), 'PV_IMAGE')):
            shutil.rmtree(os.path.join(os.path.dirname(__file__), 'PV_IMAGE'))


        for party in PARTIES_LIST:
            if not os.path.exists(os.path.join(os.path.dirname(__file__), 'PV_IMAGE', party)):
                os.makedirs(os.path.join(os.path.dirname(__file__), 'PV_IMAGE', party))

        if not os.path.exists(os.path.join(os.path.dirname(__file__), 'PV_IMAGE', 'REAL_RESULT')):
            os.makedirs(os.path.join(os.path.dirname(__file__), 'PV_IMAGE', 'REAL_RESULT'))

        if not os.path.exists(os.path.join(os.path.dirname(__file__), 'PV_IMAGE', 'ELECAM')):
            os.makedirs(os.path.join(os.path.dirname(__file__), 'PV_IMAGE', 'ELECAM'))

        for folder in os.listdir(os.path.join(os.path.dirname(__file__), 'PV_PDF')):
            for file in os.listdir(os.path.join(os.path.dirname(__file__), 'PV_PDF', folder)):
                # pages = convert_from_path(os.path.join(os.path.dirname(__file__), 'PV_PDF', folder, file), 500)
                # pages[0].save(os.path.join(os.path.dirname(__file__), 'PV_IMAGE', folder, file), 'JPEG')
                result = pdf2jpg.convert_pdf2jpg(os.path.join(os.path.dirname(__file__), 'PV_PDF', folder, file),
                                                os.path.join(os.path.dirname(__file__), 'PV_IMAGE', folder), pages="0")
                print(result)

        print('Delete that folders')

        #import shutil

        for folder in os.listdir(os.path.join(os.path.dirname(__file__), 'PV_IMAGE')):
            for small_folders in os.listdir(os.path.join(os.path.dirname(__file__), 'PV_IMAGE', folder)):
                file = os.listdir(os.path.join(os.path.dirname(__file__), 'PV_IMAGE', folder, small_folders))[0]
                tab = file.split('.')
                new_file_name = tab[0][2:] + '.' + tab[-1]
                shutil.move(os.path.join(os.path.dirname(__file__), 'PV_IMAGE', folder, small_folders, file),
                            os.path.join(os.path.dirname(__file__), 'PV_IMAGE', folder, new_file_name))
                os.rmdir(os.path.join(os.path.dirname(__file__), 'PV_IMAGE', folder, small_folders))

        


        import json
        #import os

        import requests
        from PIL import Image
        from pytesseract import image_to_string

        from variable import PARTIES_LIST


        def removeNumbers(string_numbers):
            for i, el in enumerate(string_numbers):
                if not string_numbers[-int(i) - 1].isdigit():
                    return string_numbers[-int(i - 1) - 1:]
                    break
            return string_numbers


        with open('results.json', 'w+') as f:
            f.write('[')
            for bureau_index, folder in enumerate(os.listdir(os.path.join(os.path.dirname(__file__), 'PV_IMAGE'))):
                for pv_index, image in enumerate(os.listdir(os.path.join(os.path.dirname(__file__), 'PV_IMAGE', folder))):
                    img = [str(elt) for elt in
                        image_to_string(
                            Image.open(os.path.join(os.path.dirname(__file__), 'PV_IMAGE', folder, image))).split(
                            '\n') if not elt.replace(" ", "") == ""]
                    bureau_de_Vote = img[0].replace("O", '0').replace('I', '1').replace(" ", "").split("_")[-1]
                    enrolled_number = img[1].split(':')[-1].replace("I", "1").replace(" ", "")
                    #print(bureau_de_Vote)
                    #print(enrolled_number)
                    #print(img)
                    #print(folder + image)
                    party = [int(removeNumbers(elt.replace(" ", "").replace("|", "1").replace("O", "0"))) for elt in
                            img[4:len(PARTIES_LIST) + 4]]
                    #print(party)
                    global_id = 11 * bureau_index + pv_index
                    #print(folder)
                    if folder == "ELECAM":
                        real_id, party_name = "elecam", -1
                    elif folder == "REAL_RESULT":
                        real_id, party_name = "bon", -2
                    else:
                        real_id, party_name = global_id, PARTIES_LIST.index(folder)

                    scrutateur_format = dict(scrutineerId=global_id, scrutineerName=real_id, partyNumber=party_name)
                    pv_format = dict(pvId=global_id, pollingStation=removeNumbers(bureau_de_Vote), numberOfSuscribers=enrolled_number,
                                    numberOfVoters=enrolled_number, voices=party, partyNumber=party_name,
                                    scrutineer="resource:org.cloud.elections.Scrutineer#{}".format(global_id), scrutineerName=real_id)
                    data_format = dict(id=global_id, bureau=bureau_de_Vote, nbreInscrits=enrolled_number,
                                    nbreVotants=enrolled_number,
                                    voix=party, idScrutateur=global_id,
                                    nomScrutateur=real_id, parti=party_name)
                    json.dump(data_format, f)
                    f.write(',')
                    r = requests.post('http://localhost:3000/api/Scrutineer', json=scrutateur_format)
                    r = requests.post('http://localhost:3000/api/Pv', json=pv_format)

            f.write(']')


        
        #print(variable.PARTIES_LIST)
        #print(variable.BUREAU_VOTES_NUMBER)
        #print(variable.ENROLLED_PEOPLE_NUMBER)
        #print(variable.COALITION_MODE)
        return str(status.HTTP_200_OK)
    except Exception as e:
        return str(status.HTTP_400_BAD_REQUEST), str(e)


@app.errorhandler(404)
def not_found(e):
    return str(status.HTTP_404_NOT_FOUND)


if __name__ == '__main__':
    app.run(debug=True)
