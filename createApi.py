import requests
import os
import json
import argparse 

bearer = "Bearer " + os.environ['ACCESS_TOKEN']
endpoint = "https://anypoint.mulesoft.com/apimanager/api/v1/organizations/" + os.environ['ORGID'] + "/environments/" + os.environ['ENVID'] + "/apis"
headers = {"Authorization": bearer, 'Content-Type': 'application/json'}

def parse_argument():
	parse = argparse.ArgumentParser()
	parse.add_argument("build_dir")
	args = parse.parse_args()
	return args

def loadSpecFile(fileDir):
	try:
		file = open(fileDir,)
		data = json.load(file)
		if(data['changeSpecification']):
			data = data['data']
		else:
			apiIdCreate = createAPI(data['data'])
			print ('##vso[task.setvariable variable=apiId]' + str(apiIdCreate))
			data = None
	except OSError as e:
		data = None
	return data

def assetFound(response,spec):
	apiId = None
	for assets in response['assets']:
		for apis in assets['apis']:			
			if(apis["groupId"] == spec['spec']['groupId']) and (apis["assetId"] == spec['spec']['assetId'] and (apis['instanceLabel'] == spec['instanceLabel'])):
				if((apis["assetVersion"] == spec['spec']['version'])):
					apiId = apis['id']
				else:
					apiId = patchAPI(apis['id'],spec['spec']['version'])
	return apiId

def getAPIS():
	response = requests.get(endpoint, headers=headers).json()
	return response

def createAPI(spec):
	response = requests.post(endpoint,headers=headers,json=spec).json()
	return response['id']

def patchAPI(apiId,version):
	payload = json.dumps({
		"assetVersion": version
	})
	response = requests.patch(endpoint + "/" + str(apiId),headers=headers,data=payload).json()
	return response['id']

def main():
	args = parse_argument()
	apis = getAPIS()
	spec = loadSpecFile(args.build_dir)
	if spec != None:
		apiId = assetFound(apis,spec)
		if apiId != None:
			print (str(apiId))
		else:
			apiIdCreate = createAPI(spec)
			print (str(apiIdCreate))
			
if __name__ == "__main__":
	main()
