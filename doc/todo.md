### Optimization:
- Add caching layer for STIB API data
- Get rid of Pandas/Numpy dependencies or use a lambda layer for it

### I18N :
- Add support for English locale(s)
- Add support for fr-BE locale (not available yet)
- Add support for nl-NL locale (not available yet)
    
### Functionality:
- Correctly compute waiting time when bus/tram/metro is leaving 
 in less than one minute and when bus/tram/metro leaves after midnight
- Implement error handling for API calls
- Add safety nets in dialog flow to avoid triggering wrong intents 
- Implement slots confirmation in dialog model (perhaps not)

### Publishing
- Get STIB logos
- Add detailed testing instructions
- Add detailed skill description
- Prepare app for production 
    - Setup correct logging config 
    - Use STIB API production environment

### CICD
- Add unit tests to build process
- Extend test suite
- Add code coverage to build process
- Use Public GitHub as alternative source control system

### Nice to have:
- Implement personalisation 
- Try out SSML tags
- Support name free interaction
- Redesign preferences intent as a single intent
- Implement context switching 
    - use request interceptor checking dialog state
    - store intent state in session attributes

