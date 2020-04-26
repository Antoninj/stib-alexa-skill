### Optimization:
- Add caching layer for STIB API data => validate implementation on AWS infra using elasticache (memcached) 

### I18N:
- Add support for English locale(s)
- Add support for fr-BE locale (not available yet)
- Add support for nl-NL locale (not available yet)
    
### Functionality/UX:
- Implement error handling for API calls
- Correctly compute waiting time when bus/tram/metro is leaving 
 in less than one minute and when bus/tram/metro leaves after midnight
- Add safety nets in dialog flow to avoid triggering wrong intents 

### Certification & Publishing
- Get STIB logos
- Add detailed testing instructions
- Add detailed skill description
- Prepare app for production 
    - Setup correct logging config 
    - Use STIB API production environment 
      in template configuration file
    - Use memcached Elasticache cluster configuration endpoint

### CICD
- Add Elasticache cluster to infra template
- Update codepipeline project to deploy infra template
- Add unit tests to build process
- Improve test suite

### Nice to have:
- Implement personalisation 
- Try out SSML tags to add custom sound samples
- Support name free interaction
- Redesign trip preferences intent as a single intent
- Implement context switching 
    - use request interceptor checking dialog state
    - store intent state in session attributes

