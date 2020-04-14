### Optimization:
- Cache STIB API data locally
- Get rid of Pandas/Numpy dependency or use a lambda layer for it

### I18N :
- Move hardcoded runtime intent handlers strings to data module
- Add support for English locale(s)
- Add support for fr-BE locale (not available yet)
- Add support for nl-NL locale (not available yet)
    
### Functionality:
- Correctly format arrival times (handle all scenarios) 
- Implement error handling for API calls
- Implement slots confirmation in dialog model(perhaps not)

### Publishing
- Get STIB logos
- Add detailed testing instructions
- Add detailed skill description

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

