Welcome to the AWS CodeStar 'hello world' sample project for  Alexa Skills Kit (Python)
=======================================================================================

This project helps first-time Alexa Skills Kit developers get started by providing them with a working 'hello world' skill. This project provisions a sample Alexa skill that uses the custom interaction model, an AWS Lambda function, and an AWS CodePipeline continuous integration/continuous delivery (CI/CD) pipeline.

**NOTE** : You should only make edits in the repository. Do not edit this skill directly using any other Alexa Skills Kit tools which are not integrated with this repository.

Pre-requisites
--------------
* You must already have created an [Amazon Developer account](https://developer.amazon.com/).

What's Here
-----------
* skill.json - contains the skill manifest that provides Alexa with your skill metadata. [See manifest documentation here](https://developer.amazon.com/docs/smapi/skill-manifest.html)
* interactionModels - contains interaction model files in JSON format. [See interaction model documentation here](https://developer.amazon.com/docs/smapi/interaction-model-schema.html).
  * en-US.json - contains the interaction model for the en-US locale.
* lambda - the parent folder that contains the code of all Lambda functions of this skill.
  * custom
    * hello_world.py - contains the request handling code that will be deployed to AWS Lambda function.
    * requirements.txt - contains a list of dependencies to be installed.
* buildspec.yml - used by AWS CodeBuild to package the Lambda function code to be deployed by CodePipeline using CloudFormation.
* template.yml - the template with reference to Lambda function code to be deployed by CloudFormation.
* README.md - this file.

What Do I Do Next?
------------------
* The default invocation name of your skill is 'hello python'.
* Test the 'hello world' skill in the Alexa Simulator. From your AWS CodeStar project dashboard, choose the Alexa Simulator button. You can also go to the [Alexa Skills Kit developer console](https://developer.amazon.com/alexa/console/ask), select your skill, and choose the Test tab. Enable testing and type or say, "Open hello python" or "ask hello python hello".
* Once the skill is enabled in the Alexa Simulator, it can also be invoked on an Alexa enabled device which is registered with your Amazon developer account.
* Understand the fundamental concepts of an Alexa skill. See [this video playlist](https://www.youtube.com/watch?v=hbH6gZoKcbM&list=PL2KJmkHeYQTMRyGDtVVhEnSGX6FRrkg6X).
* Configure your project repository in your favorite IDE and iterate on your skill. [See instructions for cofiguring an AWS CodeCommit repository with your IDE](https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-gc.html).
* Turn your idea into a skill. Read the documentation for [Alexa Skills Kit](https://developer.amazon.com/docs/quick-reference/custom-skill-quick-reference.html) and the [ASK SDK](https://developer.amazon.com/docs/quick-reference/use-sdks-quick-reference.html).
* Go to the [Alexa Skills Kit developer console](https://developer.amazon.com/alexa/console/ask) to submit, certify and publish your skill.

NOTE : You should only make edits in the repository. Do not edit this skill directly in the Alexa Skills Kit developer console or using any other Alexa Skills Kit tools as the skill will get out of sync with your repository.