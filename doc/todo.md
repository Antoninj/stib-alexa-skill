### Optimization:
- Get rid of Pandas/Numpy or use a lambda layer for it
- Add local caching of STIB API data
- Move hardcoded runtime intent handlers strings to data module

### Functionality:
- Format correctly arrival times (handle all scenarios) 
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
- Add correct tags on AWS

### Nice to have:
- Implement personalisation 
- Try out SSML tags
- I18N :
    - Support EN
    - Support NL
- Support name free interaction
- Redesign preferences intent as a single intent
- Implement context switching

