### Local debugging with ngrok
`./ngrok http 3001`

### Generate requirements
`pipenv run pipenv_to_requirements -f`     

### Validate CF template
`aws cloudformation validate-template --template-body file://template.yml`

### I18N
1. Create new locale support  
`pybabel init -i lambda/custom/core/locales/base.pot -l fr_FR -o lambda/custom/core/locales/fr-FR/LC_MESSAGES/base.po`

2. Extract strings to be translated  
`pybabel extract lambda/custom/core/data/data.py -o lambda/custom/core/locales/base.pot`  

3. Update locales info  
`pybabel update -i lambda/custom/core/locales/base.pot -l fr_FR -o lambda/custom/core/locales/fr-FR/LC_MESSAGES/base.po`
`pybabel update -i lambda/custom/core/locales/base.pot -l en_GB -o lambda/custom/core/locales/en-GB/LC_MESSAGES/base.po`
`pybabel update -i lambda/custom/core/locales/base.pot -l fr_CA -o lambda/custom/core/locales/fr-CA/LC_MESSAGES/base.po`

4. Compile to machine code  
`pybabel compile -i lambda/custom/core/locales/fr-FR/LC_MESSAGES/base.po -o lambda/custom/core/locales/fr-FR/LC_MESSAGES/base.mo`
`pybabel compile -i lambda/custom/core/locales/fr-CA/LC_MESSAGES/base.po -o lambda/custom/core/locales/fr-CA/LC_MESSAGES/base.mo`
`pybabel compile -i lambda/custom/core/locales/en-GB/LC_MESSAGES/base.po -o lambda/custom/core/locales/en-GB/LC_MESSAGES/base.mo`

### Automated integration tests generation with Urutu
`urutu create-test`

### Run unit tests
`python -m unittest discover -p '*_test.py'`

### Doc coverage with interrogate
`interrogate lambda/custom -q --ignore-init-method --ignore-init-module --ignore-module  --ignore-regex handle --ignore-regex can_handle --generate-badge assets/images/`

### CF stack name
alexa-skill-vpc-cache-infrastructure

