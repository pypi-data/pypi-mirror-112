# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_france',
 'data_france.admin',
 'data_france.data',
 'data_france.management',
 'data_france.management.commands',
 'data_france.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.1.0,<3.2.0']

setup_kwargs = {
    'name': 'data-france',
    'version': '0.12.2',
    'description': "Paquet agrégeant des données administratives publiques pour en rendre l'utilisation facile.",
    'long_description': "data-france\n=============\n\nUn ensemble de données administratives et géographiques pour la France. Elle double comme application Django\npour permettre l'intégration aisée de ces données.\n\n\nInstaller le paquet\n-------------------\n\nInstallez ce paquet avec pip::\n\n  pip install data-france\n\n\nImporter les données\n--------------------\n\nPour importer les données, appliquez les migrations et utilisez la commande de management::\n\n  ./manage.py update_data_france\n\n\nModèles\n--------\n\nL'application django comporte les modèles suivants :\n\n* `Commune`\n\n  * Inclut les communes délégués / communes associées / arrondissements PLM /\n    secteurs électoraux PLM\n  * Les différents types d'entités sont différenciés par le champ `type`\n\n* `EPCI`\n\n  * Il s'agit des EPCI à fiscalité propre : CA, CC, CU et métropoles\n  * N'inclut pas encore les EPT du Grand Paris\n\n* `Departement` et `Region` pour les départements et régions comme\n  circonscriptions administratives de l'État\n* `CollectiviteDepartementale` et `CollectiviteRegionale` pour les départements\n  et régions comme collectivités territoriales :\n\n  * La métropole de Lyon (aux compétences départementales) est référencée comme\n    une collectivité départementale ;\n  * les collectivités territoriales uniques (par exemple l'Assemblée de Corse)\n    sont référencées comme des collectivités régionales (cela inclut, de façon\n    contre-intuitive, le département de Mayotte) ;\n  * À noter que comme le conseil de Paris est déjà référencé comme une\n    `Commune`, il n'est pas référencé de nouveau comme collectivité\n    départementale.\n\n* Les codes postaux\n\nToutes ces entités (sauf les codes postaux, et les collectivités régionales,\ndont la géométrie est systématiquement celle de la région correspondante)\nviennent avec une géometrie et les articles + charnière.\n\nVues\n----\n\nUne vue de recherche renvoyant les résultats en JSON est disponible, par défaut\nà l'URL `chercher/communes/` (en utilisant le paramètre GET `q`). Il est\npossible d'obtenir les résultats au format geojson en ajoutant le paramètre GET\n`geojson` à une valeur non vide.\n\n\nAutres remarques\n----------------\n\n**ATTENTION** : Ce paquet ne fonctionne que si votre projet Django utilise\n **PostGIS** car il utilise certaines fonctionnalités propres à PostgreSQL.\n",
    'author': 'Arthur Cheysson',
    'author_email': 'arthur@cheysson.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aktiur/data-france',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
