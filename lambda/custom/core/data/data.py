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

SKILL_NAME = "Horaires STIB"

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
    "votre trajet favori ou modifier votre trajet favori à tout moment. Que souhaitez-vous faire?"
)
SKILL_DESCRIPTION_WITH_PREFERENCES_REPROMPT = _("Comment puis-je vous aider?")
ASK_FOR_PREFERENCES = _("Souhaitez-vous enregistrer vos préférences maintenant?")
ASK_FOR_PREFERENCES_REPROMPT = "Voulez-vous configurer votre trajet favori maintenant?"


###################################################
#              Amazon builtin intents             #
###################################################

"""""" """""" """""" """
    Yes intent
""" """""" """""" """"""
ELLICIT_LINE_PREFERENCES = _(
    "D'accord, c'est parti. Les lignes du réseau STIB sont numérotées de 1 à 98."
    " Quelle ligne utilisez vous d'habitude?"
)
ELLICIT_LINE_PREFERENCES_REPROMPT = _("Quel est votre ligne STIB habituelle?")

"""""" """""" """"
Help intent
""" """""" """"""
HELP = _(
    "Demandez par exemple 'Quand passe le prochain bus' pour obtenir des informations en temps réél sur les prochains horaires de passage."
    "Vous pouvez également dire 'Modifie mes préférences' pour modifier votre trajet favori. Que souhaitez-vous faire?"
)
HELP_REPROMPT = _(
    "Demandez par exemple 'Quand passe le prochain bus' pour obtenir des informations en temps réél sur les prochains horaires de passage."
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

"""""" """""" """"
Error handler
""" """""" """"""
ERROR = _(
    "Désolé, je n'ai pas compris votre requête. Pouvez vous répeter s'il vous plait."
)
ERROR_REPROMPT = _("Désolé, je n'ai pas compris. Pouvez vous répeter s'il vous plait.")

###################################################
#                CUSTOM INTENTS                   #
###################################################

"""""" """""" """""
favorite line intent
""" """""" """""" ""
ELLICIT_DESTINATION_PREFERENCES = (
    "C'est noté. Dans quelle direction prenez vous le {} {}, {} ou {}?"
)
ELLICIT_DESTINATION_PREFERENCES_REPROMPT = "Dans quelle direction allez vous, {} ou {}?"

"""""" """""" """""
favorite stop intent
""" """""" """""" ""
PREFERENCES_SAVED = (
    "Merci, vos préférences ont été correctement sauvegardées."
    " Vous prenez donc le {} {} à l'arret {} direction {}."
)

"""""" """""" """""" """""" """"
Get arrival times intent
""" """""" """""" """""" """"""
FIRST_ARRIVAL_TIME_INFO = "Le prochain {} {} en direction de {} passe dans {}."
SECOND_ARRIVAL_TIME_INFO = "Le suivant passe dans {}."
NO_INFORMATION_FOUND = (
    "Désolé, je n'ai pas trouvé d'informations pour le trajet demandé."
)
FAREWELL = "Bonne journée!"

"""""" """""" """""" """""" """
Save trip preferences intent
""" """""" """""" """""" """"""
