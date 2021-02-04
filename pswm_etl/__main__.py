
import os
import re
import json
import multigenomic_api
from dotenv import load_dotenv
from utils import file_handler
from utils.arguments import load_arguments

if __name__ == '__main__':

    identifiers_user = os.getenv("IDENTIFIER_USER")
    identifiers_pass = os.getenv("IDENTIFIERS_PASS")
    multigenomic_user = os.getenv("MULTIGENOMIC_USER")
    multigenomic_pass = os.getenv("MULTIGENOMIC_PASS")

    load_dotenv()
    arguments = load_arguments()

    input_path = arguments.inputdir
    output_file = arguments.outputfile
    log_file = arguments.log

    html_file_names = file_handler.find_html_files(input_path)

    multigenomic_api.connect('regulondbmultigenomic', 'mongodb://localhost:27017')

    schema_data = {"classAcronym": "ECOLI", "collectionName": "pswm", "organism": "ECOLI", "subClassAcronym": "MXC",
                   "collectionData": []}

    for html_file in html_file_names:
        print(html_file)

        re_tfname = rf"({input_path}\/([^\/]*)\/)"
        tfname = re.match(re_tfname, html_file)
        print(tfname.group(2))

        transcription_factors = multigenomic_api.transcription_factors.find_by_name(tfname.group(2))
        print(transcription_factors)
        if len(transcription_factors) == 1:

            with open(html_file, 'rb') as html_file_fp:
                content = html_file_fp.read().decode(encoding='unicode_escape')

                # Matching the matrix
                re_matrix = r"(A\t[0-9]+..*\nC\t[0-9]+..*\nG\t[0-9]+..*\nT\t[0-9]+..*)"
                matrix = re.search(re_matrix, content)
                if matrix != None:
                    print(matrix.group(0))

                # Matchsing Sites
                re_sites = r"((>site..*[ATGCactg]+)\n;\n; Matrix)"
                sites = re.search(re_sites, content, re.DOTALL)
                if sites != None:
                    tfbinding = sites.group(1)
                    tfbs = tfbinding.replace(";\n; Matrix", "")
                    print(tfbs)

                # getting the command
                re_command = r"Command:</b> (matrix-quality..*)\n"
                command = re.search(re_command, content)
                if command != None:
                    print(command.group(1))

                tfdata ={
                        "_id": str(transcription_factors),
                        "name": str(tfname.group(2) + "Matrix"),
                        "transcriptionFactor_id": str(transcription_factors),
                        "metadata_id": "Id_Temporal",
                        "matrix":{
                            "parameters": "",
                            "data": (matrix.group(0) + tfbs + command.group(1))
                                },
                        "logoPath": "",
                        "htmlFilePath": html_file,
                        "citations": [{
                            "publications_id": "",
                            "evidences_id": ""
                        }],
                        "notes": ""
                    }

                schema_data["collectionData"].append(tfdata)


        else:
            message2 = ("El nombre del TF no fue encontrado" + "/n")
            with open(log_file, "a") as filelog:
                json.dump(message2, filelog, indent=4)


    with open(output_file, "w") as filetf:
        json.dump(schema_data, filetf, indent=4)
