# django-podle
[![Python 3.9](https://img.shields.io/badge/python-3.7|3.8|3.9-blue.svg)](https://www.python.org/downloads/release/python-390/) 
[![Django 2.2](https://img.shields.io/badge/django-2.2-blue.svg)](https://docs.djangoproject.com/en/2.2/)
[![Python CI](https://github.com/briefmnews/django-podle/actions/workflows/workflow.yaml/badge.svg)](https://github.com/briefmnews/django-podle/actions/workflows/workflow.yaml)
[![codecov](https://codecov.io/gh/briefmnews/django-podle/branch/main/graph/badge.svg?token=w8N0eR6uLr)](https://codecov.io/gh/briefmnews/django-podle)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)  
Integration with [Podle.io](https://podle.io/) podcast app.  
See Podle documentation [here](https://docs.podle.io/).

## Installation
Install with [pip](https://pip.pypa.io/en/stable/):
```shell
pip install -e git://github.com/briefmnews/django-podle.git@main#egg=django-podle
```

## Setup
In order to make `django-podle` works, you'll need to follow the steps below.


### Settings
First you need to add the following configuration to your settings:
```python
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',

    'podle',
    ...
)
```

### Migrations
Next, you need to run the migrations in order to update your database schema.
```shell
python manage.py migrate
```

### Mandatory settings
Here is the list of all the mandatory settings:
```python
PODLE_AUTH_TOKEN: api key to consume the api
PODLE_NEWSLETTER_NAME: name of the newsletter. Useful for RSS feed
```

### Optional settings
Here is the list of all the mandatory settings:
```python
PODLE_RSS_FEED_GROUP_NAME: group name for creating / deleting private RSS feed.
```

## Webhook
You can give an url to Podle to get a webhook when the newsletter audio file is created.
The webhook will be post to `{YOUR_DOMAIN}/podle/webhook`.
A signal called `audio_file` is sent when receiving the webhook.

In case of success, if the audio file is created with an existing `newsletter` object:
```python
audio_file.send(sender=Newsletter, success=True, audio_url=serializer.validated_data["newsletter_url"], newsletter=newsletter)
```

In case of an error:
```python
audio_file.send(sender=Newsletter, success=False, errors=serializer.errors)
```

## How to use?
### Create or update a newsletter
Here is a quick example of how to create an audio file with podle.
```python
from podle.models import Newsletter

json_content = {
  "correspondent": "John Doe or johndoe.mp3",
  "title": "Gestion de l’eau | Talibans | Correspondance amoureuse",
  "description": "Dans Brief.me ce week-end, la gestion de l’eau en France, les talibans, la rumba congolaise et la correspondance amoureuse d’un détenu.\nTest Thomas",
  "voiceGender": "female",
  "intro": "Brief.me : édition du 10 mai 2021",
  "sections": [
    {
      "title": "",
      "articles": [
        {
          "title": "",
          "body": "Dans Brief.me ce week-end, la gestion de l’eau en France, les talibans, la rumba congolaise et la correspondance amoureuse d’un détenu.\nTest Thomas",
          "voiceGender": "female",
          "source": ""
        }
      ]
    },
    {
      "title": "La gestion de l’eau en France",
      "articles": [
        {
          "title": "",
          "body": "Les entreprises françaises de gestion de l’eau et des déchets Suez et Veolia ont annoncé lundi être parvenues à un accord de principe pour leur rapprochement. Suez s’opposait depuis l’an dernier aux offres de rachat de Veolia. Cette opération intervient alors que la gestion de l’eau en France, fortement déléguée par les communes à des opérateurs privés dans les années 1990, connaît une « remunicipalisation » depuis quelques années.À l’origine. Au XIXe siècle, l’industrialisation et la persistance d’épidémies dans les grandes villes font de la gestion de l’eau un sujet de préoccupation majeur. Les communes, qui en sont chargées depuis la Révolution française, se dotent progressivement de réseaux de distribution d’eau salubre à partir de la moitié du XIXe siècle. Se développent un service public, qui dessert gratuitement les fontaines publiques, et un service privé et payant d’eau à domicile. Bénéficier de l’eau à domicile est toutefois le privilège d’une minorité aisée. Les communes ont recours à des compagnies privées de distribution d’eau, auxquelles elles confient le service à domicile, en échange de quoi ces entreprises participent au financement des fontaines publiques. Les premières sociétés créées sont la Compagnie générale des eaux en 1853 et la Lyonnaise des eaux en 1880. Les communes rurales commencent à s’équiper dans les années 1930. Le raccordement sera lent : il faut attendre la fin des années 1980 pour que la quasi-totalité des Français bénéficient de l’eau potable à domicile.Les dates clés. 1964. La loi de 1964 sur l’eau est le premier texte qui organise la gestion de l’eau à l’échelle nationale, alors que sa consommation progresse et que le niveau de pollution s’accroît avec l’urbanisation et le développement de l’industrie et de l’agriculture intensive. La loi organise la gestion de l’eau autour de six grands bassins fluviaux en métropole (voir la carte). Elle crée une agence de l’eau pour chaque bassin, chargée de percevoir des redevances auprès des personnes publiques ou privées, dès lors qu’elles prélèvent de l’eau ou la polluent, et de financer ainsi la préservation de la ressource et la lutte contre la pollution. Les redevances permettent par exemple aux collectivités de financer les stations d’épuration des eaux usées. Alors que la France ne comptait que 300 stations d’épuration avant l’adoption de la loi de 1964, plus de 2 100 stations étaient recensées en 1970 et 11 500 en 1990, selon deux rapports parlementaires de 2003.1997. En 1997, la Lyonnaise des eaux et la Compagnie financière de Suez, une société française qui a exploité la concession du canal égyptien de Suez, fusionnent et deviennent le groupe Suez-Lyonnaise des eaux (rebaptisé Suez en 2001). Le groupe recentre ses activités sur les services aux collectivités, dont la gestion de l’eau. Il concurrence ainsi sur le marché la Compagnie générale des eaux (dont la filiale consacrée à l’environnement deviendra Veolia) et Saur. En 1995, 75 % de la population, soit plus de 46 millions d’habitants, sont approvisionnés en eau par un opérateur privé, la Compagnie générale des eaux alimentant à elle seule 25 millions de personnes, rapporte Christelle Pezon, chercheuse dans le domaine de l’eau potable, dans sa thèse en 2000. Les communes (ou les intercommunalités), auxquelles incombent la distribution de l’eau potable et l’assainissement et qui sont propriétaires des infrastructures, peuvent choisir d’exploiter le service selon plusieurs modes, dont la régie – en le gérant directement – et la délégation de service public – en le confiant à un opérateur privé.2000. La ville de Grenoble vote en 2000 le retour en régie du service de l’eau et de l’assainissement, qui était géré depuis 1989 par une filiale de la Lyonnaise des eaux. Cette décision fait suite à une affaire de corruption impliquant l’opérateur et le maire de l’époque, Alain Carignon, pour laquelle il a été condamné par la justice. Plusieurs villes ont fait le choix d’un retour à la régie, comme Paris, Brest et Nice, dans les années 2010. Cette « remunicipalisation » de la gestion de l’eau intervient après des constatations de mauvais entretien des réseaux ou d’écarts de prix entre les deux modes de gestion. En 2018, seuls 31 % des services publics d’eau potable étaient gérés par délégation, mais ils approvisionnaient une majorité (57 %) de la population, selon un rapport publié ce mois-ci par l’Office français de la biodiversité, un établissement public.2015. Le Conseil constitutionnel, l’instance chargée de contrôler la conformité des lois à la Constitution, rend une décision en mai 2015 affirmant que l’eau « répond à un besoin essentiel de la personne » et « qu’aucune personne en situation de précarité » ne peut en être privée. Il avait été saisi après une demande du distributeur Saur, assigné en justice pour avoir coupé l’eau à un client entre avril 2013 et septembre 2014 pour un impayé de près de 280 euros. Saur contestait l’interdiction, introduite par une loi de 2013, pour les distributeurs d’eau de procéder à des coupures dans une résidence principale en cas de défaut de paiement des factures, et ce tout au long de l’année. Le Conseil constitutionnel ayant validé la constitutionnalité de la loi, Saur est condamné dans cette affaire en octobre 2015. Plusieurs décisions de justice rendues par la suite ont statué également sur l’interdiction de toute réduction du débit d’eau par les distributeurs.Le concept. En France, l’eau qui alimente les robinets est captée majoritairement dans les nappes souterraines ou dans des plans et cours d’eau. Cette eau est rendue potable au sein d’une usine de potabilisation à travers différents procédés, dont la filtration et la désinfection. L’eau est testée pour vérifier que les teneurs de diverses substances (plomb, arsenic, pesticides, etc.) sont inférieures aux normes sanitaires établies par l’UE. L’eau potable est ensuite stockée, souvent dans des châteaux d’eau, afin de disposer de réserves en cas de variations de la demande. L’eau potable est acheminée jusqu’aux usagers grâce à un réseau de canalisations. Environ 20 % de l’eau potable est perdue lors de sa distribution à cause de fuites, selon Eau de France, le service public de l’information sur l’eau. Les eaux usées, versées au « tout-à-l’égout », sont assainies dans une station d’épuration, avant d’être rejetées, le plus souvent dans des rivières. En 2018, la consommation moyenne d’eau potable était de 148 litres par jour et par habitant, selon l’Office français de la biodiversité.",
          "voiceGender": "female",
          "source": ""
        }
      ]
    },
    {
      "title": "On rembobine la semaine",
      "articles": [
        {
          "title": "",
          "body": "Iran. La France, l’Allemagne et le Royaume-Uni ont exprimé mercredi leur « grande préoccupation » concernant l’annonce faite la veille par l’Iran du lancement d’un processus pour produire de l’uranium enrichi à 60 %, contre 20 % actuellement. Depuis le retrait en 2018 des États-Unis de l’accord de 2015 sur le nucléaire iranien, qui prévoyait que l’Iran n’enrichisse pas l’uranium à plus de 3,67 % pendant 15 ans, l’Iran s’est affranchi progressivement des limites fixées à ses capacités nucléaires.Viticulture. La FNSEA, le principal syndicat agricole, a annoncé mercredi qu’au moins un tiers de la production viticole française allait être perdue cette année à cause du gel, représentant une perte de 2 milliards d’euros de chiffre d’affaires. 10 des 13 régions métropolitaines ont connu la semaine dernière un épisode de gel exceptionnel, provoquant d’importants dégâts dans les cultures viticoles. Le Premier ministre, Jean Castex, avait annoncé samedi dernier que « tous les mécanismes de soutien » seraient activés.Sécurité. Le Parlement a définitivement adopté jeudi la proposition de loi sur la « sécurité globale », soutenue par le gouvernement. L’Assemblée nationale s’est prononcée en seconde lecture par 75 voix contre 33 en faveur de ce texte très critiqué par les syndicats de journalistes et plusieurs ONG comme Amnesty International, qui estime qu’« entre les mains d’un gouvernement autoritaire, une telle loi deviendrait une dangereuse arme de surveillance et de répression de la population ». Le groupe des députés socialistes a annoncé hier son intention de saisir le Conseil constitutionnel, l’instance chargée de contrôler la conformité des lois à la Constitution.Russie. La Maison-Blanche a annoncé jeudi l’adoption d’une série de sanctions financières contre la Russie, ainsi que l’expulsion de 10 diplomates russes en poste aux États-Unis. Cette décision vise à répondre aux ingérences russes dans les élections américaines de 2020 et à une cyberattaque massive ayant touché des agences fédérales et entreprises américaines, attribuée à la Russie. Le président américain, Joe Biden, qui s’est entretenu avec son homologue russe Vladimir Poutine cette semaine, l’a également appelé à la « désescalade » en Ukraine, où un conflit oppose depuis 2014 séparatistes pro-russes et armée ukrainienne dans l’est du pays.Violences sexuelles. Le Parlement a adopté jeudi soir, par un ultime vote à l’unanimité à l’Assemblée nationale, une proposition de loi visant à mieux protéger les mineurs contre les crimes et délits sexuels. Le texte fixe un seuil de non-consentement à 15 ans, en deçà duquel tout acte de pénétration sexuelle commis par un adulte sera automatiquement considéré comme un viol. Ce seuil est de 18 ans en cas d’inceste. « Avant 15 ans, plus aucun adulte agresseur ne pourra se prévaloir du consentement d’un mineur », s’est félicité jeudi le ministre de la Justice, Éric Dupond-Moretti.Covid-19. Environ 35 500 cas quotidiens de Covid-19 avaient été détectés en moyenne sur sept jours jeudi, contre près de 34 900 une semaine plus tôt, et plus de 5 900 personnes se trouvaient en réanimation, soit 200 de plus en une semaine, selon le ministère de la Santé. Jeudi soir, près de 12 millions de personnes avaient reçu au moins une dose de vaccin contre le Covid-19, selon Santé publique France, un organisme public dépendant du ministère de la Santé. La vaccination est étendue depuis lundi aux personnes de 55 ans et plus. Le Premier ministre, Jean Castex, a annoncé mardi la suspension des vols depuis et vers le Brésil, en raison de la forte circulation dans le pays du variant P1, très contagieux.",
          "voiceGender": "female",
          "source": ""
        }
      ]
    },
    {
      "title": "Talibans",
      "articles": [
        {
          "title": "",
          "body": "La Maison-Blanche a annoncé mardi que le retrait des 2 500 soldats américains encore déployés en Afghanistan s’achèverait d’ici le 11 septembre. Le précédent président américain, Donald Trump, s’était engagé à retirer les troupes américaines avant le 1er mai 2021, lors d’un accord signé en février 2020 avec les talibans. « Taliban » est le pluriel de « taleb », un mot désignant en arabe et en pachto un étudiant en théologie, ce qui explique les deux orthographes au pluriel avec ou sans « s ». Au début des années 1990 se forme en Afghanistan un mouvement de combattants islamistes composé en grande partie d’anciens étudiants des écoles coraniques, lui donnant leur nom. Ces combattants prennent le pouvoir dans le pays en 1996, imposant de nombreuses restrictions à la population. En 2001, ils sont destitués lors d’une intervention dirigée par les États-Unis qui les accusent de protéger le mouvement terroriste Al-Qaïda. Depuis, les talibans ont repris le contrôle de larges portions du pays. Ils ont revendiqué de nombreux attentats ces dernières années.",
          "voiceGender": "female",
          "source": ""
        }
      ]
    },
    {
      "title": "Ça vaut un clic",
      "articles": [
        {
          "title": "",
          "body": "La rumba congolaise. La rumba congolaise, un style musical des deux Congo, est candidate à l’inscription sur la liste du patrimoine immatériel de l’humanité. Dans un article, RFI Musique revient sur les quelque 80 ans d’existence de la rumba congolaise, inspirée de la musique cubaine, ses évolutions et la place qu’elle occupe dans la société, jusqu’à devenir représentative « de l’identité du peuple congolais ». Cet article s’accompagne d’une playlist réalisée par RFI pour découvrir ce style particulièrement dansant. Alicia, 16 ans, escort. Alicia, 20 ans, raconte, dans l’émission de France Culture « Les Pieds sur Terre », comment elle est devenue escort pendant près de deux mois à 16 ans. Après la découverte impérieuse de sa sexualité et une rencontre fortuite, elle se prostitue via les applications Tinder et Snapchat, sans jamais tomber dans le piège des proxénètes ni de la drogue. « Si moi j’ai pu le faire, combien d’autres filles de mon âge, voire plus jeunes, l’ont fait sous l’influence d’un proxénète ? », se demande-t-elle dans un témoignage plein de lucidité. « Mon oncle ». À travers une belle série photo en noir et blanc publiée sur le site du journal suisse Le Temps, le photographe français Corentin Fohlen rend hommage à son oncle, surnommé « l’original de la famille ». Il dresse un portrait tendre de son parrain, qu’il voit comme un « génie génial », « sans limite », et le représente couvert de boue, en pleine manifestation des gilets jaunes ou encore en chaman, tout nu sur une pirogue. Lettres d’amour. Dans « The Letter Room », un court-métrage diffusé sur Arte.tv, un agent pénitentiaire aux États-Unis est affecté au courrier des détenus. Il doit tout examiner avant la distribution, mais a interdiction de lire les lettres en entier. Sauf qu’il va être intrigué par la correspondance d’une femme, Rosita, à un détenu condamné à mort. À la lecture de ces lettres d’amour, pleines de poésie et de romantisme, il fait une découverte qui va le pousser à rendre visite à Rosita. « The Letter Room » est en lice pour l’Oscar du meilleur court-métrage.",
          "voiceGender": "female",
          "source": ""
        }
      ]
    },
    {
      "title": "",
      "articles": [
        {
          "title": "",
          "body": "Vous voilà « briefés » sur l’actu de la semaine. Passez un bon week-end à vivre d’amour et d’eau fraîche.",
          "voiceGender": "female",
          "source": ""
        }
      ]
    }
  ]
}

Newsletter.objects.create_or_update_newsletter(YourModel, json_content)
```

### Private RSS feed
You can create an RSS feed for your users to use with podcast applications like Pocket Casts or Overcast.

You can handle RSS feed in the admin or with code:

#### Create a private RSS feed
```python
from podle.models import RssFeed

RssFeed.objects.create(user=user)
```

#### Get an existing private RSS feed
```python
from podle.models import RssFeed

RssFeed.objects.get_rss_feed(user=user)
```

#### Delete a private RSS feed
```python
from podle.models import RssFeed

RssFeed.objects.get(user=user).delete()
```

#### Create or delete Rss feeds
Adding a single user or users to the group defined in the PODLE_RSS_FEED_GROUP_NAME setting
will create or delete the rss feed for those users.
