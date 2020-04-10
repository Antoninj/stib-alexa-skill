# -*- coding: utf-8 -*-

# Resolving gettext as _ for module loading.
from gettext import gettext as _

SKILL_NAME = "Horaires STIB"

# Launch request intent
WELCOME_NEW_USER = _("Bienvenue dans la skill horaires STIB!")
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

# Yes intent
ELLICIT_LINE_PREFERENCES = _(
    "Allons-y. Quelle ligne du réseau STIB utilisez vous lors de votre trajet quotidien?"
)

ELLICIT_LINE_PREFERENCES_REPROMPT = _("Quel est le numéro de votre ligne favorite?")

# Save trip preferences intent


# Help intent
HELP = _("Quelle ligne du réseau STIB utilisez vous lors de votre trajet quotidien?")
HELP_REPROMPT = _("Quel est le numéro de votre ligne favorite?")

# Cancel & Stop intents
STOP = _("D'accord. A bientôt!")

# Fallback intent
FALLBACK = _(
    "La skill horaires STIB n'est pas en mesure de vous aider pour cela. Comment puis-je vous aider?"
)
FALLBACK_REPROMPT = _("Comment puis-je vous aider?")

# Error handler
ERROR = _(
    "Désolé, je n'ai pas compris votre requête. Pouvez vous répeter s'il vous plait."
)
ERROR_REPROMPT = _("Désolé, je n'ai pas compris. Pouvez vous répeter s'il vous plait.")
