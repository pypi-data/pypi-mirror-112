La librairie niiif-niiif crée et publie le manifeste IIIF d'une donnée Nakala.

# Installation
 
Pour utiliser le script, utilisez de préférence un gestionnaire d'environnement Python tel que [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

```bash
# Vous pouvez définir le nom de l'environnement Python à votre convenance avec le paramètre -n.
conda create -n niiif-niiif python=3.8
# Activez l'environnement
conda activate niiif-niiif
# Installez la librairie niiif
pip install niiif
```

# Utilisation

Le script a besoin pour fonctionner des clés d'API d'un compte utilisateur Nakala ayant des droits d'écriture sur 
la donnée Nakala pour laquelle vous souhaitez créer un manifeste. Cette clé d'API est à créer et à copier 
depuis le profil du compte Nakala.

```bash
# Activez l'environnement (si ce n'est pas déjà fait)
conda activate niiif-niiif 
# Pour créer le manifeste de la donnée Nakala dont l'ID = 10.34847/nkl.12121212
python -m niiif -apikey 12345678-12345678-1234578-12345678 -dataid 10.34847/nkl.12121212
```

La librairie :

- Crée un manifeste IIIF à partir des fichiers JPEG ou TIFF de la donnée Nakala
- Ajoute le fichier metadata.json, contenant le manifeste, sur la donnée Nakala

Vous pouvez ensuite copier l'URL du fichier metadata.json dans Nakala et l'utiliser dans une visionneuse IIIF 
(ex. [Mirador](https://mirador-dev.netlify.app/__tests__/integration/mirador/)).

