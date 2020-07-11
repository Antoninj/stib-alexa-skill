### Documentation:
- Improve docstrings 

### I18N:
- Add support for fr-BE locale (not available yet)
- Add support for nl-NL locale (not available yet)
    
### Functionality/UX:
- Correctly compute waiting times when bus/tram/metro is leaving
 in less than one minute and when bus/tram/metro leaves after midnight
- Add safety nets in dialog flow to avoid triggering wrong intents

### Certification & Publishing 
- Prepare app for production:
    - Deploy lambda in custom VPC => ok
    - Use memcached Elasticache cluster configuration endpoint in env variables => ok

### CICD / Tooling
- Extend test suite
- Update CodePipeline project to deploy infra template (elasticache and network)  => not for now
- Add unit tests to build process => not for now
- Add code coverage => not for now
- Add code quality 

### Next features
- Add network updates by line
- Implement personalisation
- Support name free interaction
- Redesign trip preferences intent as a single intent
- Implement context switching
    - use request interceptor checking dialog state
    - store intent state in session attributes
