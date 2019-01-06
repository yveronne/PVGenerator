import os
from pdf2jpg import pdf2jpg

from variable import PARTIES_LIST

import shutil
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

import shutil

for folder in os.listdir(os.path.join(os.path.dirname(__file__), 'PV_IMAGE')):
    for small_folders in os.listdir(os.path.join(os.path.dirname(__file__), 'PV_IMAGE', folder)):
        file = os.listdir(os.path.join(os.path.dirname(__file__), 'PV_IMAGE', folder, small_folders))[0]
        tab = file.split('.')
        new_file_name = tab[0][2:] + '.' + tab[-1]
        shutil.move(os.path.join(os.path.dirname(__file__), 'PV_IMAGE', folder, small_folders, file),
                    os.path.join(os.path.dirname(__file__), 'PV_IMAGE', folder, new_file_name))
        os.rmdir(os.path.join(os.path.dirname(__file__), 'PV_IMAGE', folder, small_folders))
