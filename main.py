import requests
import os
from bs4 import BeautifulSoup

#Variables and such are in spanish to save time on edition.

# Website URL of Quakeworld Quake 1 maps database.
url = "https://maps.quakeworld.nu/all/"

# Destination folder for the downloaded maps  THIS HAS TO BE SET IN ORDER FOR THE SCRIPT TO WORK!
carpeta_destino = r"C:\Users\luism\OneDrive\Escritorio\qwmaps"

# GET Request to the website
response = requests.get(url)

# Checking if the request is successful
if response.status_code == 200:
    # Obtaining content from the website.
    contenido = response.text

    # Checking HTML content with BeautifulSoup
    soup = BeautifulSoup(contenido, "html.parser")

#Fila = Rows , It's important to know the rows gotta be checked.
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
                    # Save the file in the destination folder
                    ruta_archivo = os.path.join(carpeta_destino, nombre_archivo)
                    with open(ruta_archivo, "wb") as archivo:
                        archivo.write(response.content)

                    print(f" {nombre_archivo} file downloaded successfully.")
                else:
                    print(f" {nombre_archivo} wasn't downloaded")
else:
    print("Website can't be accessed")