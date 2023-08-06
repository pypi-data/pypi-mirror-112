import requests
import json
import argparse
import sys

MANIFEST_FILE_DESCRIPTION = 'IIIF manifest'

def process_args():
    parser = argparse.ArgumentParser(description="Creates JSON IIIF manifests for Nakala datas")
    parser.add_argument("-dataid", "--data_identifier", help="Nakala data identifier")
    parser.add_argument("-apikey", "--api_key", help="Nakala user API key")
    args = parser.parse_args()
    if args.data_identifier is None:
        print('*** Usage error: -dataid or --data_identifier should be specified ')
        parser.print_usage()
        sys.exit(1)
    if args.api_key is None:
        print('*** Usage error: -apikey or --api_key should be specified ')
        parser.print_usage()
        sys.exit(1)
    return args


def get_data_metadata(args):
    dataIdentifier = args.data_identifier
    try:
        # The response could be an error message
        response = requests.get('https://api.nakala.fr/datas/' + dataIdentifier)
    except Exception as err:
        print(err)
    return response


def get_manifest_data_sha1_if_exists(dataMetadataJSON):
    files = dataMetadataJSON['files']
    manifest_sha1 = None
    for file in files:
        if file['name'] == 'metadata.json' and file['description'] == MANIFEST_FILE_DESCRIPTION:
            manifest_sha1 = file['sha1']
    return manifest_sha1


def delete_manifest(args, sha1):
    dataIdentifier = args.data_identifier
    try:
        response = requests.delete('https://api.nakala.fr/datas/' + dataIdentifier + '/files/' + sha1,
                                   headers=uploadsAPIHeaders)
        if response.status_code == 204:
            print('Info : metadata.json file deleted for data id ' + dataIdentifier)
    except Exception as err:
        print(err)
    return response


def create_data_manifest(args, dataMetadataJSON):
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
    # 10.34847/nkl.66bdx361
    # 10.34847/nkl.c1d1w5fj

    manifest = None

    try:
        canvases = []
        dataIdentifier = args.data_identifier

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
                    fileMetadata = requests.get("https://api.nakala.fr/iiif/" + dataIdentifier + "/" + str(sha1) +
                                                "/info.json")
                    fileMetadataJSON = fileMetadata.json()
                    width = fileMetadataJSON['width']
                    height = fileMetadataJSON['height']
                except Exception as err:
                    print(err)
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
                                         "@id": "https://api.nakala.fr/iiif/" + dataIdentifier + "/" + str(sha1) +
                                                "/full/full/0/default.jpg" ,
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
        # Nakala (qui contient le SHA1 du fichier) mais il faudrait pourvoir modifier le fichier une fois déposé
        # sur Nakala, ce qui n'est évidemment pas possible.

        sequenceId = 'https://www.nakala.fr/iiif/' + dataIdentifier + '/sequence/normal'

        manifestData = {"@context": "http://iiif.io/api/presentation/2/context.json",
                "@id": "https://api.nakala.fr/data/" + dataIdentifier,
                "@type": "sc:Manifest",
                "attribution": dataMetadataJSON["owner"]["username"],
                "label": dataCitation,
                "sequences": [{
                    "@id": sequenceId,
                    "@type": "sc:Sequence",
                    "canvases": canvases
                }]
                }

        manifest = json.dumps(manifestData, indent=4)
    except Exception as err:
        print(err)
    return manifest


def upload_manifest_file(args, manifest):
    # A FAIRE : Vérifier que le fichier n'existe pas déjà et le remplacer si nécessaire.
    files = {'file': ('metadata.json', manifest)}
    url = 'https://api.nakala.fr/datas/uploads'
    try:
        response = requests.post(url, files=files, headers=uploadsAPIHeaders)
        print(response.text)
        if response.status_code == 201:
            sha1 = response.json()['sha1']
            print(sha1)
            url = 'https://api.nakala.fr/datas/' + args.data_identifier + '/files'
            data = {
                'sha1': sha1,
                'description': MANIFEST_FILE_DESCRIPTION
            }
            dataJSON = json.dumps(data)
            response = requests.post(url, headers=filesAPIHeaders, data=dataJSON)
            print(response.text)
    except Exception as err:
        print(err)


def main():
    global uploadsAPIHeaders
    global filesAPIHeaders

    args = process_args()
    uploadsAPIHeaders = {
        'accept': 'application/json',
        'X-API-KEY': args.api_key,
    }

    filesAPIHeaders = {
        'accept': 'application/json',
        'X-API-KEY': args.api_key,
        'Content-Type': 'application/json',
    }

    response = get_data_metadata(args)
    if response.status_code == 200:
        dataMetadataJSON = response.json()
        manifest_sha1 = get_manifest_data_sha1_if_exists(dataMetadataJSON)
        if manifest_sha1 is not None:
            delete_manifest(args, manifest_sha1)
        manifest = create_data_manifest(args, dataMetadataJSON)
        if manifest is not None:
            upload_manifest_file(args, manifest)
        else:
            print("The manifest could not be created")
    else:
        print(response.json()['message'])


if __name__ == '__main__':
    main()
