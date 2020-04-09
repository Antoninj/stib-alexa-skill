# Lambda endpoint
{
  "manifest": {
    "apis": {
      "custom": {
        "endpoint": {
          "uri": "${DailyCommuteFunction.Alias}"
        }
      }
    }
  }
}

# I18N

1. pybabel extract lambda/custom/core/data/data.py -o lambda/custom/core/locales/base.pot    
2. pybabel init -i lambda/custom/core/locales/base.pot -l fr_FR -o lambda/custom/core/locales/fr-FR/LC_MESSAGES/base.po
3. pybabel compile -i lambda/custom/core/locales/fr-FR/LC_MESSAGES/base.po -o lambda/custom/core/locales/fr-FR/LC_MESSAGES/base.mo
