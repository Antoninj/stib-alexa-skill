# -*- coding: utf-8 -*-

# Resolving gettext as _ for module loading.
from gettext import gettext as _

SKILL_NAME = "Horaires STIB"

# Launch request intent
WELCOME = _("Bienvenue dans horaires STIB!")

# Help intent
HELP = _("Quelle ligne du réseau STIB utilisez vous lors de votre trajet quotidien?")
HELP_REPROMPT = _("Quel est le numéro de votre ligne favorite?")

# Cancel & Stop intents
STOP = _("A la prochaine!")

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
