# Composite Actions for Mule Applications

## Introduction
Composite actions were made for reusing among workflows when working with Mule Applications. Independent jobs are written to fully customize pipeline, avoiding extra steps and improving speed delivery.

## Jobs implemented
### Test
* [Maven SureFire test report](#1)
* [Maven test](#2)
* [SonarQube code quality testing](#3)
* [Newman integration testing](#4)
### Build
* [JAR building](#5)
* [Release version upgrade](#6)
### Deploy
* [CloudHub deployment](#7)
* [Exchange deployment](#8)
* [API Manager registration](#9)

## Usage
In this section, examples of all jobs with detailed description are presented. Also, at the end of this README, example pipelines are shown to explain how to gather all this jobs.
## Testing
### 1) Maven SureFire test report <a name="1"></a>
This job run Maven's test goal with SureFire plugin to generate test reports. The report generated with [SureFire plugin](https://maven.apache.org/surefire/maven-surefire-plugin/) will be published by this job.
#### Preconditions
* SureFire Maven plugin must be configured in project's pom.xml file.
* Created a settings.xml file and exported it with name "settings".
#### Parameters
| Name  | Description | Example |
| ------------- |:-------------:|:----------|
| testParams      | Parameters given to mvn test command     | -Dmule.key=xxx -Dmule.env=dev
#### Example usage
```
name: Test
    runs-on: ubuntu-latest

    steps:
      - name: Test Mule App
        uses: manuelrbrizi/deploy-to-cloudhub-action/test@main
        with:
          testParams: -Dmule.env=dev -Dmule.key=${{ secrets.MULE_KEY }}
```
### 2) Maven test <a name="2"></a>
This job run Maven's `test` goal, with the specified parameters. In this job, Maven SureFire isn't necessary due that no report is generated.
#### Preconditions
* Created a settings.xml file and exported it with name "settings".
#### Parameters
| Name  | Description | Example |
| ------------- |:-------------:|:----------|
| testParams      | Parameters given to mvn test command     | -Dmule.key=xxx -Dmule.env=dev
#### Example usage
```
- name: Test Mule App
uses: manuelrbrizi/deploy-to-cloudhub-action/testWithoutReports@main
with:
  testParams: -Dmule.env=dev -Dmule.key=${{ secrets.MULE_KEY }}
```
### 3) SonarQube code quality testing <a name="3"></a>
This job run a local Docker container with a SonarQube server and test the project's code with Mule specific rules. The documentation about this Docker image is available [here](https://github.com/mulesoft-catalyst/mule-sonarqube-plugin).
#### Preconditions
* Created a settings.xml file and exported it with name "settings".
#### Parameters
| Name  | Description | Example |
| ------------- |:-------------:|:----------|
| sourcesPath      | Path to .xml Mule Configuration Files     | src/main/mule
#### Example usage
```
- name: sonarQubeTesting
uses: manuelrbrizi/deploy-to-cloudhub-action/sonarqube@main
with:
  sourcesPath: src/main/mule
```
### 4) Newman integration testing <a name="4"></a>
This job do integration testing with [Newman](https://learning.postman.com/docs/running-collections/using-newman-cli/command-line-integration-with-newman/). 
#### Preconditions
* Having a Postman Collection.
#### Parameters
| Name  | Description | Example |
| ------------- |:-------------:|:----------|
| collectionName      | Name of the Postman collection     | postman_collection.json
#### Example usage
```
- name: newmanIntegrationTesting
uses: manuelrbrizi/deploy-to-cloudhub-action/newman@main
with:
  collectionName: postman_collection.json
```
## Build
### 5) JAR building <a name="5"></a>
This job use Maven `package` goal to build a deployable JAR. It also export it to be deployed by `Deploy to CloudHub (with artifact)` job.
#### Preconditions
* Created a settings.xml file and exported it with name "settings".
#### Parameters
None
#### Example usage
```
name: Update release version
runs-on: ubuntu-latest

steps:
  - name: updateVersion
    uses: manuelrbrizi/deploy-to-cloudhub-action/buildJar@main
```
### 6) Release version upgrade <a name="6"></a>
This job use Maven build helper to get the current version of the asset and upgrade it in one unit. The new version will be commited to the repository.
#### Preconditions
* Created a settings.xml file and exported it with name "settings".
#### Parameters
None
#### Example usage
```
name: Update release version
runs-on: ubuntu-latest

steps:
  - name: updateVersion
    uses: manuelrbrizi/deploy-to-cloudhub-action/updateVersion@main
```
## Deploy 
### 7) A) CloudHub deployment (from artifact) <a name="7"></a>
This job use a .jar artifact (which is previously created and exported by `Build JAR` job. This JAR is located at the root folder with the Mule Application, so it can be deployed with the `mule:deploy` goal.
#### Preconditions
* Created a settings.xml file and exported it with name "settings".
* `Build JAR` job finished.
#### Parameters
| Name  | Description | Example |
| ------------- |:-------------:|:----------|
| deployParams      | Parameters given to mvn deploy command     | -Dmule.key=xxx -Dmule.env=dev
#### Example usage
```
name: Deploy to CloudHub
needs: [buildJar]
runs-on: ubuntu-latest

steps:
  - name: deployToCloudhub
    uses: manuelrbrizi/deploy-to-cloudhub-action/deployToCloudhub@main
    with:
      deployParams: -Dusername=${{ secrets.USERNAME }} -Dpassword=${{ secrets.PASSWORD }} -Dmule.env=dev -Dmule.key=${{ secrets.MULE_KEY }} -Dserver=cloudhub -Dregion=us-east-2 -Dworkers=1 -DworkerType=MICRO -DappName=spending-git -Danypoint.platform.client_id=${{ secrets.ANYPOINT_CLIENT_ID }} -Danypoint.platform.client_secret=${{ secrets.ANYPOINT_CLIENT_SECRET }} -Denvironment=Playground
```
### 7) B) CloudHub deployment (build and deploy)
This job simply runs the `deploy` goal of Maven, which builds and deploy the App.
#### Preconditions
* Created a settings.xml file and exported it with name "settings".
#### Parameters
| Name  | Description | Example |
| ------------- |:-------------:|:----------|
| deployParams      | Parameters given to mvn deploy command     | -Dmule.key=xxx -Dmule.env=dev
#### Example usage
```
name: Deploy to CloudHub
needs: [updateVersion]
runs-on: ubuntu-latest

steps:
  - name: deployToCloudhub
    uses: manuelrbrizi/deploy-to-cloudhub-action/buildAndDeployToCloudhub@main
    with:
      deployParams: -Dusername=${{ secrets.USERNAME }} -Dpassword=${{ secrets.PASSWORD }} -Dmule.env=dev -Dmule.key=${{ secrets.MULE_KEY }} -Dserver=cloudhub -Dregion=us-east-2 -Dworkers=1 -DworkerType=MICRO -DappName=spending-git -Danypoint.platform.client_id=${{ secrets.ANYPOINT_CLIENT_ID }} -Danypoint.platform.client_secret=${{ secrets.ANYPOINT_CLIENT_SECRET }} -Denvironment=Playground
```
### 8) Exchange deployment <a name="8"></a>
This job run Maven's deploy goal with a previously generated artifact for Exchange deployment.
#### Preconditions
* If the current version of the asset is already deployed to Exchange, the `Upgrade release version` must be run before this job.
* Created a settings.xml file and exported it with name "settings".
#### Parameters
| Name  | Description | Example |
| ------------- |:-------------:|:----------|
| projectName      | artifact name generated in `target/` folder (without .jar)    | app-with-dependencies
#### Example usage
```
    name: Deploy to Exchange
    needs: [updateVersion] 
    runs-on: ubuntu-latest

    steps:
      - name: deployToExchange
        uses: manuelrbrizi/deploy-to-cloudhub-action/deployToExchange@main
        with:
          projectName: spending-eapi
```
##### *Note: the 'needs:' directive is only if we want to update the Release version before deploying to Exchange.*
### 9) API Manager registration <a name="9"></a>
This job register the API in API Manager. If it isn't registered, this job creates it. If it is registered, this job updates the current instance depending on the specification file provided. This job also exports an artifact named `apiId.txt` which contains the API Id generated by API Manager. An example of getting this file in any job is provided below.
#### Preconditions
* Created a settings.xml file and exported it with name "settings".
* An API specification file with JSON format.
#### Parameters
| Name  | Description | 
| :-------------: |:-------------:|
| ORGID      | Organization Id   
| ENVID      | Environment Id   
| CLIENT_ID      | Client Id   
| CLIENT_SECRET      | Client secret  
| specPath | Path to the API specification .json file
#### Example usage
```
- name: deployToAPIManager
  uses: manuelrbrizi/deploy-to-cloudhub-action/apiManager@main
  with:
    ORGID: ${{ secrets.ORGID }}
    ENVID: ${{ secrets.ENVID }}
    CLIENT_ID: ${{ secrets.CLIENT_ID }}
    CLIENT_SECRET: ${{ secrets.CLIENT_SECRET }}
    specPath: spec/spec.json
```
#### Example spec/spec.json
```
{
   "providerId":null,
   "changeSpecification": true,
   "data":{
      "instanceLabel": "My API",
      "spec":{
         "assetId":"spending-eapi",
         "groupId":"8047b9c3-dd3a-4b49-b414-136f87448c77",
         "version":"1.0.3"
      },
      "endpoint": {
         "deploymentType":"CH",
         "isCloudHub":null,
         "muleVersion4OrAbove":true,
         "proxyUri":null,
         "referencesUserDomain":null,
         "responseTimeout":null,
         "type":"raml",
         "uri": null
      }
   }
}
```
#### Example getting apiId.txt file and saving a environment variable with API ID
```
- name: Download apiId.txt
uses: actions/download-artifact@v2
with:
  name: apiId

- run: |
  echo "API_ID=$(cat apiId.txt)" >> $GITHUB_ENV
```
## Examples
Note: none of this examples use approvals, however, these jobs can be used within environments with different rules. To learn how to add approvals to your workflows, see [this post](https://timheuer.com/blog/add-approval-workflow-to-github-actions/).
### Simple Test, Build & Deploy to CloudHub
File: [simple-deploy-to-ch.yml](simple-deploy-to-ch.yml)
![First example](/images/1.png "First example")

### Test, Upgrade version, Build & Deploy to Exchange
File: [upgrade-and-deploy-xc.yml](upgrade-and-deploy-xc.yml)
![Second example](/images/2.png "Second example")

### Complete workflow
File: [complete-workflow.yml](complete-workflow.yml)
![Third example](/images/3.png "Third example")
