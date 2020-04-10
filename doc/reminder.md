### Lambda endpoint
`{
  "manifest": {
    "apis": {
      "custom": {
        "endpoint": {
          "uri": "${DailyCommuteFunction.Alias}"
        }
      }
    }
  }
}`

### I18N
1. Create new locale support  
`pybabel init -i lambda/custom/core/locales/base.pot -l fr_FR -o lambda/custom/core/locales/fr-FR/LC_MESSAGES/base.po`

2. Extract strings to be translated  
`pybabel extract lambda/custom/core/data/data.py -o lambda/custom/core/locales/base.pot`  

3. Update locales info  
`pybabel update -i lambda/custom/core/locales/base.pot -l fr_FR -o lambda/custom/core/locales/fr-FR/LC_MESSAGES/base.po`

4. Compile to machine code  
`pybabel compile -i lambda/custom/core/locales/fr-FR/LC_MESSAGES/base.po -o lambda/custom/core/locales/fr-FR/LC_MESSAGES/base.mo`
