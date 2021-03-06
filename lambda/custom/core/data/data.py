# -*- coding: utf-8 -*-

# Resolving gettext as _ for module loading.

#   Copyright 2020 Antonin Jousson
#
#  Licensed under the Apache License, Version 2.0 (the "License").
#  You may not use this file except in compliance with the License.
#  A copy of the License is located at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  or in the "license" file accompanying this file. This file is
#  distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
#  OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the
#  License.

from gettext import gettext as _

SKILL_NAME = _("Horaires STIB")

###################################################
#                Launch Request                   #
###################################################

"""""" """""" """""" """
Launch request intent 
""" """""" """""" """"""
WELCOME_NEW_USER = _("Bienvenue dans la skill Horaires STIB!")
WELCOME_RETURNING_USER = _("Bonjour.")
SKILL_DESCRIPTION_WITHOUT_PREFERENCES = _(
    "Je ne connais pas encore votre trajet favori."
)
SKILL_DESCRIPTION_WITH_PREFERENCES = _(
    "Vous pouvez demander des informations en temps réél concernant "
    "votre trajet favori, modifier vos préférences ou encore demander de l'aide. Que souhaitez-vous faire?"
)
SKILL_DESCRIPTION_WITH_PREFERENCES_REPROMPT = _("Comment puis-je vous aider?")
ASK_FOR_PREFERENCES = _("Souhaitez-vous enregistrer vos préférences maintenant?")
ASK_FOR_PREFERENCES_REPROMPT = _(
    "Voulez-vous configurer votre trajet favori maintenant?"
)


###################################################
#              Amazon builtin intents             #
###################################################

"""""" """""" """""" """
    Yes intent
""" """""" """""" """"""
ELLICIT_LINE_PREFERENCES = _(
    "D'accord, c'est parti. Les lignes du réseau STIB sont numérotées de 1 à 98. "
    "Quelle ligne utilisez vous d'habitude?"
)
ELLICIT_LINE_PREFERENCES_REPROMPT = _("Quel est votre ligne STIB habituelle?")

"""""" """""" """"
Help intent
""" """""" """"""
HELP = _(
    "Dites par exemple 'Quand est-ce que passe mon prochain bus?' pour obtenir des informations en temps réél sur les prochains horaires de passage. "
    "Vous pouvez également dire 'Modifie mes préférences' pour modifier votre trajet favori. Que souhaitez-vous faire?"
)
HELP_REPROMPT = _(
    "Dites par exemple 'Quand est-ce que passe mon prochain bus?' pour obtenir des informations en temps réél sur les prochains horaires de passage. "
    "Vous pouvez également dire 'Modifie mes préférences' pour modifier votre trajet favori. Que souhaitez-vous faire?"
)

"""""" """""" """""" """""
Cancel & Stop intents
""" """""" """""" """""" ""
STOP = _("D'accord. A bientôt!")

"""""" """""" """""
Fallback intent
""" """""" """""" ""
FALLBACK = _(
    "La skill Horaires STIB n'est pas en mesure de vous aider pour cela. Comment puis-je vous aider?"
)
FALLBACK_REPROMPT = _("Comment puis-je vous aider?")

"""""" """""" """
Error handlers
""" """""" """"""

GENERIC_ERROR = _(
    "Désolé, je n'ai pas compris votre requête. Pouvez vous répeter s'il vous plait."
)
GENERIC_ERROR_REPROMPT = _(
    "Désolé, je n'ai pas compris. Pouvez vous répeter s'il vous plait."
)

OPEN_DATA_API_ERROR = _(
    "Désolé, je ne suis pas en mesure de récupérer les informations de la STIB pour le moment."
)
OPEN_DATA_API_ERROR_REPROMPT = _(
    "Désolé, je ne suis pas en mesure de récupérer les informations de la STIB pour le moment."
)

###################################################
#                CUSTOM INTENTS                   #
###################################################

"""""" """""" """""" """
Set favorite line intent
""" """""" """""" """"""
ELLICIT_DESTINATION_PREFERENCES = _(
    "C'est noté. Dans quelle direction prenez vous le {} {}, {} ou {}?"
)
ELLICIT_DESTINATION_PREFERENCES_REPROMPT = _(
    "Dans quelle direction allez vous, {} ou {}?"
)

"""""" """""" """""" """
Set favorite stop intent
""" """""" """""" """"""
PREFERENCES_SAVED = _(
    "Merci, vos préférences ont été correctement sauvegardées."
    " Vous prenez donc le {} {} à l'arret {} direction {}."
)

"""""" """""" """""" """""" """"
Get arrival times intent
""" """""" """""" """""" """"""
FIRST_ARRIVAL_TIME_INFO = _(
    "Le prochain {} {} en direction de {} passe à l'arrêt {} dans {}."
)
SECOND_ARRIVAL_TIME_INFO = _("Le suivant passe dans {}.")
NO_INFORMATION_FOUND = _(
    "Désolé, je n'ai pas trouvé d'informations pour le trajet demandé."
)
FAREWELL = _("Bon voyage")

"""""" """""" """""" """""" """
Save trip preferences intent
""" """""" """""" """""" """"""


###################################################
#                MODEL                            #
###################################################
NOT_FOUND = _("INFORMATION MANQUANTE")
ARRIVAL_TIME_DAYS_HOURS_MINUTES_SECONDS = _(
    "{} jours, {} heures, {} minutes et {} secondes"
)
ARRIVAL_TIME_HOURS_MINUTES_SECONDS = _("{} heures, {} minutes et {} secondes")
ARRIVAL_TIME_MINUTES_SECONDS = _("{} minutes et {} secondes")
ARRIVAL_TIME_SECONDS = _("{} secondes")
