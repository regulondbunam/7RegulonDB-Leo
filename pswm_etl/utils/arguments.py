import argparse

def load_arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description="Argumentos",
                                     epilog="Consulta argumentos")
    parser.add_argument(
        "-i", "--inputdir",
        help='Directorio de entrada de los reportes HTML de las matrices posición peso',
        required=True
    )

    parser.add_argument(
        "-o", "--outputfile",
        help='Archivo que contiene la información extraída de cada TF',
        required=False

    )

    parser.add_argument(
        "-l", "--log",
        help="Directorio que contiene el registro de los TFs no encontrados en la base de datos",
        required=False
    )

    arguments = parser.parse_args()
    return arguments