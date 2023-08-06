import requests
import json

from settings import (
    X_API_KEY
)

# Attention les identifiants des documents peuvent être des DOI (10.34847/nkl.c1d1w5fj)
# ou des Handle (11280/b4d935c2).
# Cas d'un Carnet de Anatole Le Braz : ALBM1
# https://nakala.fr/10.34847/nkl.c1d1w5fj
# ID d'un des fichiers TIFF du carnet : 10.34847/nkl.c1d1w5fj/a79248c84cef396c1f2ddc57b7e028f90b4b2b1c
# a79248c84cef396c1f2ddc57b7e028f90b4b2b1c est le SHA1
# présent dans les résultats de la requête :
# curl -X GET "https://api.nakala.fr/datas/10.34847%2Fnkl.c1d1w5fj/files" -H  "accept: application/json"
# Renvoie (entre autres):
#
#   {
#     "name": "CRBC_ALBM1_027.tif",
#     "extension": "tif",
#     "size": 12424178,
#     "mime_type": "image/tiff",
#     "sha1": "847ea669a1d7daf92208d31d4d95f4c0032b0754",
#     "embargoed": "2021-04-29T00:00:00+02:00",
#     "description": null,
#     "humanReadableEmbargoedDelay": []
#   }
#
# L'API Image de IIIF pour ce fichier TIFF est accessible depuis :
# https://api.nakala.fr/iiif/10.34847/nkl.c1d1w5fj/a79248c84cef396c1f2ddc57b7e028f90b4b2b1c/full/max/0/default.jpg
# https://api.nakala.fr/iiif/10.34847/nkl.c1d1w5fj/a79248c84cef396c1f2ddc57b7e028f90b4b2b1c
# https://api.nakala.fr/iiif/10.34847/nkl.c1d1w5fj/a79248c84cef396c1f2ddc57b7e028f90b4b2b1c/info.json

# 10.34847/nkl.37afk8kn
dataIdentifier = '10.34847/nkl.66bdx361'
# A faire : Vérifier si cette URI doit être déréférençable

canvases = []

# ex. https://www.nakala.fr/iiif/11280/b4d935c2
iiif_base_image_request_uri = "https://api.nakala.fr/iiif/" + dataIdentifier
# ex. https://www.nakala.fr/iiif/11280/b4d935c2/full/full/0/default.jpg
iiif_image_request_uri = iiif_base_image_request_uri + '/full/full/0/default.jpg'

dataMetadata = requests.get('https://api.nakala.fr/datas/' + dataIdentifier)
dataMetadataJSON = dataMetadata.json()
# !!!!!!!!!!!!!! il faut récupérer le titre Nakala ou Dublin Core
# {'value': 'ALBM1', 'lang': None, 'typeUri': 'http://www.w3.org/2001/XMLSchema#string', 'propertyUri': 'http://nakala.fr/terms#title'}

dataCitation = dataMetadataJSON['citation']
files = dataMetadataJSON['files']

for file in files:
    sha1 = file['sha1']
    if file['mime_type'] in {'image/tiff', 'image/jpeg'}:
        # Pour récupérer la taille en pixel du fichier
        fileMetadataJSON = None
        width = 100
        height = 100
        try:
            fileMetadata = requests.get("https://api.nakala.fr/iiif/" + dataIdentifier + "/" + str(sha1) + "/info.json")
            fileMetadataJSON = fileMetadata.json()
            width = fileMetadataJSON['width']
            height = fileMetadataJSON['height']
        except:
            None
        canvasURI = 'https://api.nakala.fr/iiif/' + dataIdentifier + "/canvas/" + str(sha1)
        canvases.append({"@type": "sc:Canvas",
                         "@id": canvasURI,
                         "label": file["name"],
                         "width": width,
                         "height": height,
                         "images": [{
                             "@type": "oa:Annotation",
                             "motivation": "sc:painting",
                             "on": canvasURI,
                             "resource": {
                                 "@id": "https://api.nakala.fr/iiif/" + dataIdentifier + "/" + str(sha1) + "/full/full/0/default.jpg" ,
                                 "@type": "dctypes:Image",
                                 "format": file['mime_type'],
                                 "width": width,
                                 "height": height,
                                 "service": {
                                     "profile": "http://iiif.io/api/image/2/level2.json",
                                     "@context": "http://iiif.io/api/image/2/context.json",
                                     "@id": 'https://api.nakala.fr/iiif/' + dataIdentifier + "/" + str(sha1)
                                 }
                             }
                         }]
                         }
                        )

# @id devrait être modifié pour correspondre à l'URL de téléchargement du fichier metadata.json sur
# Nakala mais il faudrait pourvoir modifier le fichier une fois déposé sur Nakala, ce qui n'est évidemment
# pas possible.

sequenceId = 'https://www.nakala.fr/iiif/' + dataIdentifier + '/sequence/normal'

manifestData = {"@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": "https://api.nakala.fr/data/" + dataIdentifier,
        "@type": "sc:Manifest",
        "attribution": dataMetadataJSON["owner"]["fullname"],
        "label": dataCitation,
        "sequences": [{
            "@id": sequenceId,
            "@type": "sc:Sequence",
            "canvases": canvases
        }]
        }

manifest = json.dumps(manifestData, indent=4)

uploadsHeaders = {
    'accept': 'application/json',
    'X-API-KEY': X_API_KEY,
    # Information erronée de la documentation de l'API Nakala...
    # 'Content-Type': 'multipart/form-data',
    # 'Content-Type': 'application/json'
}

filesHeaders = {
    'accept': 'application/json',
    'X-API-KEY': X_API_KEY,
    # Information erronée de la documentation de l'API Nakala...
    # 'Content-Type': 'multipart/form-data',
    'Content-Type': 'application/json',
}

# D:\ubo\Downloads\curl-7.77.0-win64-mingw\bin>curl.exe -X POST "https://api.nakala.fr/datas/10.34847%2Fnkl.66bdx361/files" -H  "accept: application/json" -H  "X-API-KEY: a6ae940e-ab46-0c67-fa8f-44773d57feb1" -H  "Content-Type: application/json" -d "{  \"sha1\": \"98ba5c2f3d288dd37fb957429b0ebe5fc78f6853\",  \"description\": \"string\",  \"embargoed\": \"string\"}"
# {"code":200,"message":"File added"}

# A FAIRE : Vérifier que le fichier n'existe pas déjà et le remplacer si nécessaire....

files = {'file': ('metadata.json', manifest)}
url = 'https://api.nakala.fr/datas/uploads'
try:
    response = requests.post(url, files=files, headers=uploadsHeaders)
    print(response.text)
    if response.status_code == 201:
        sha1 = response.json()['sha1']
        print(sha1)
        url = 'https://api.nakala.fr/datas/' + dataIdentifier + '/files'
        data = {
            'sha1': sha1,
            'description': 'IIIF manifest'
        }
        dataJSON = json.dumps(data)
        response = requests.post(url, headers=filesHeaders, data=dataJSON)
        print(response.text)
except Exception as err:
    print(err)
