# Wedge Library

## Démarrage rapide

```bash
$ pip install wedge-lib
```
### Configuration pour certains services

#### MailService
TBD
#### GoogleMapService
TBD
#### YousignService
TBD

## Development

### Installation

```bash
$ pipenv sync --dev
```

### Update dependencies

```bash
$ pipenv update --dev
```

### Run test

```bash
$ pytest
```

### Before commit

Pour éviter de faire échouer le CI, lancer la commande:

```bash
$ ./before_commit.zsh
```

### Publier manuellement sur PyPI

Après avoir committer et pousser:
 
1. tagguer une version dans GitHub.
2. mettre à jour la version dans le fichier `setup.cfg` avec le tag créé.
3. créer le package
    ```bash
    $ rm -rf build dist wedge_lib.egg-info
    $ WEDGELIB_VERSION=<version> python setup.py sdist bdist_wheel
    ```
4. mettre à jour sur TestPypi
    ```bash
    $ twine upload --repository testpypi dist/*
    ```
5. Si tout est ok, mettre à jour sur Pypi
    ```bash
    $ twine upload dist/*
    ```
   
### Utiliser W en mode dev depuis un autre projet (ex: csback)

Créer un lien symbolique vers le w qui va être modifié:
```bash
rm -rf <External Libraries>/site-packages/w
```
```bash
ln -s <Absolute path du projet w local>/w <External Libraries>/site-packages/.
```

Supprimer le lien symbolique et utiliser la version officielle de w :
```bash
unlink <External Libraries>/site-packages/w
```
```bash
pipenv uninstall wedge-lib && pipenv install wedge-lib
```




