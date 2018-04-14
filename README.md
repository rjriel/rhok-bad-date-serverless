# Bad Date App - Backend

This is the code for the supporting (serverless) functions for Bad Date App created for the Random Hacks of Kindness RHoK #8 Hackathon.

## Use Case

The application has two actors (actors: humans who interact to a system): End users, and moderators

* End users
  - Create accounts
  - Create reports
  - View their own reports in full
  - Edit their own reports
  - View select portions of reports that are approved by moderators
  - Contact organization of the moderators through the application based on their reports
* Moderators
  - Create curated or modified versions of full reports from end users which are presented to the public
  - Correspond with end users regarding reports

## Components

The components of the system are as follows:
* Static web page stored in a companion repository https://github.com/rjriel/rhok-bad-date-serverless
  - The web application deploys as a static page to an [Amazon S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html)
* [Amazon API Gateway](https://aws.amazon.com/api-gateway/?nc2=h_m1) using schema in [swagger.json](swagger.json)
* [Lambda functions](https://aws.amazon.com/lambda) in /src, where each function is an app.py file in its folder
* [DynamoDB](https://aws.amazon.com/dynamodb/) database (which are accessed by the aforementioned Lambda functions)

