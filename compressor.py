from PIL import Image, ImageFile
 
# Classe "Image" importada da biblioteca "PIL" usada para comprimir as imagens

import os

# Biblioteca "os" usada para manipular arquivos do sistema

import datetime

# Biblioteca "datetime" usada para manipular datas usadas nos scripts
# String de formatação para as datas
date_str_formatter = "%d/%m/%Y"

# Caminho para a pasta de input
input_folder = "./input"

# Caminho para a pasta de output
output_folder = "./output"

# Extensões permitidas a serem buscadas
extensions = [
    "jpg",
    "jpeg",
    "JPG",
    "JPEG",
    "png",
    "PNG",
    "TIFF",
    "tif",
    "tiff",
    "TIF",
]


def process_info(file_name, file_path):
    name, extension = os.path.splitext(file_name)
    file_created_at = os.path.getctime(file_path)
    file_updated_at = os.path.getmtime(file_path)
    file_size = os.path.getsize(file_path)
    # Formata o valor recebido das datas para um valor legível
    created_at_readable = datetime.datetime.fromtimestamp(file_created_at).strftime(
        date_str_formatter
    )
    updated_at_readable = datetime.datetime.fromtimestamp(file_updated_at).strftime(
        date_str_formatter
    )
    # Cria os dicionários com as informações dos arquivos encontrados
    return {
        "name": name,
        "extension": extension,
        "createdAt": created_at_readable,
        "updatedAt": updated_at_readable,
        "size": int(file_size / 1024 / 1024),
    }


def process_files(folder, files,index=None):
    # Retorna os dicionários com informações dos arquivos
    # Cria data de hoje formatada para validação
    # today = datetime.datetime.today().strftime(date_str_formatter)
        for file in files:
            # Valida se a extensão arquivo atual consta no array de extensões permitidos
            if file["extension"].replace(".", "") in extensions:
                # print(file)

                # Compara data de criação do arquivo no servidor é a mesma de hoje
                # if file["createdAt"] == today:
                # Usa a classe Image da biblioteca PIL para abrir o arquivo atual percorrido

                image_to_reduce = None
                try:
                    image_to_reduce = Image.open(f"{folder}/{file["name"] + file["extension"]}")
                except Exception:
                    print("gerou erro")
                    continue

                # Valida a extensão do arquivo para direciona-lo ao processamento correto
                if file["extension"] in [
                    ".jpg",
                    ".jpeg",
                    ".JPG",
                    ".JPEG",
                    ".png",
                    ".PNG",
                ]:
                    # Comprimi o arquivo atual optimizando sua qualidade e diminuindo o seu tamanho, mantendo um minimo padrão para evitar perda de qualidade
                    # Salva o arquvo comprimido na pasta destino (Em testes sendo a pasta de "output")

                    image_to_reduce.save(
                        f"{folder}/!{file["name"] + file["extension"]}",
                        optimize=True,
                        quality=10,
                    )
                else:
                    try:
                        image_to_reduce.save(
                            f"{folder}/{file["name"] + file["extension"]}",
                            compression="tiff_lzw",
                            tiffinfo={317: 2, 278: 1},
                        )
                    except Exception:
                        image_to_reduce.save(
                            f"{folder}/@{file["name"] + file["extension"]}",
                            compression="tiff_lzw",
                            tiffinfo={317: 2, 278: 1},
                        )
                        image_to_reduce.close()
                        print("save")
                        os.remove(f"{folder}/{file["name"] + file["extension"]}")
                        print("remove")
                        os.rename(f"{folder}/@{file["name"] + file["extension"]}", f"{folder}/{file["name"] + file["extension"]}")


def get_files(folder):
    # Parametro: folder (str): Caminho para a pasta de input.
    # Parametro: files_info (none): informação dos arquivos recuperados para utilização recursiva.
    # Retorna: Lista de dicionários contendo informações sobre os arquivos.
    files_info = []
    try:
        # Lista arquivos da pasta, recupera seus nomes e concatena com o caminho da pasta
        for file_name in os.listdir(folder):
            file_path = os.path.join(folder, file_name)
            # print(file_path)

            if os.path.isfile(file_path):
                files_info.append(process_info(file_name, file_path))

            # Verifica se o arquivo não é uma pasta e cria as variaveis com as informações: nome, extensão, data de criação e data de atualização
            if os.path.isdir(file_path):
                input_folder_files = get_files(file_path)
                process_files(file_path, input_folder_files)

    except Exception as err:
        print(f"Erro ao processar: {err}")

    return files_info


get_files(input_folder)
