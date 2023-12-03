import requests
import os
import time
import csv
from bs4 import BeautifulSoup

# Website URL of Quakeworld Quake 1 maps database.
url = "https://maps.quakeworld.nu/all/"

# Destination folder for the downloaded maps
carpeta_destino = "./qwmaps"

# CSV file path
csv_file = "./qwmaps/mapas_descargados.csv"

# Function that verifies and/or create the source folder for the maps
def verificar_carpeta_destino():
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
        print(f"Carpeta {carpeta_destino} creada.")

# Function that writes the downloaded map to the CSV file
def escribir_a_csv(nombre_archivo):
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([nombre_archivo])

# GET Request to the website
response = requests.get(url)

# Checking if the request is successful
if response.status_code == 200:
    # Obtaining content from the website.
    contenido = response.text

    # Checking HTML content with BeautifulSoup
    soup = BeautifulSoup(contenido, "html.parser")

    # Finding all the rows with download links
    filas = soup.find_all("tr")

    # For each row found.
    for fila in filas:
        # Find the elements of the row (Filename, Filesize, Date)
        elementos = fila.find_all("td")

        # Verify if the row contain the necessary elements
        if len(elementos) == 3:
            # Obtain the file name.
            nombre_archivo = elementos[0].text.strip()

            # Verify if the filename is a bsp file (compiled map)
            if nombre_archivo.endswith(".bsp"):
                # Get the download link
                enlace_descarga = elementos[0].find("a")["href"]

                # Build the complete download URL.
                url_descarga = url + enlace_descarga

                # GET Request for downloading the file (Response)
                response = requests.get(url_descarga)

                # Successful Download verification (status code 200)
                if response.status_code == 200:
                    # Verify and create the destination folder if it doesn't exist
                    verificar_carpeta_destino()

                    # Save the file in the destination folder
                    ruta_archivo = os.path.join(carpeta_destino, nombre_archivo)
                    with open(ruta_archivo, "wb") as archivo:
                        archivo.write(response.content)

                    # Write the downloaded map to the CSV file
                    escribir_a_csv(nombre_archivo)

                    print(f" {nombre_archivo} file downloaded successfully.")
                else:
                    print(f" {nombre_archivo} wasn't downloaded")
                    time.sleep(5)  # 5 second pause between download
else:
    print("Website can't be accessed")
