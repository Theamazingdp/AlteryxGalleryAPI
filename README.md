#AlteryxGalleryAPI

AlteryxGalleryAPI is a python client helper used for connecting to the Alteryx Workflow Gallery.

It includes methods that can request Gallery information, send workflow execution commands, monitor
job status, and retrieving the desired workflow output.

The official Alteryx API documentation can be found at: https://gallery.alteryx.com/api-docs/

##Setup and Install
In order to access the Gallery you must obtain an API key, secret and you must have the URL to your Alteryx Gallery.

Install the package by cloning the repository, "cd" into the populartimes directory and run pip install.

Note: This library is not avaliable through via PyPI and must be installed locally and placed in your working directory.

##USAGE
`from AlteryxGalleryAPI import AlteryxGalleryAPI`

`client_key = 'your_client_key_here'
 client_secret = 'your_client_secret_here'
 gallery_url = 'your_gallery_url'`
 
 `x = Gallery('your_gallery_url', apiKey, apiSecret)`
 
### x.subscription()

 GET request that returns all workflows in a subscription
 
 endpoint = /v1/workflows/subscription
 
###x.questions(appID)
 GET request that returns the questions for the given Alteryx Analytics App
 
 endpoint = /v1/workflows/{appId}/questions/
 
###x.executeWorkflow(appID)
 POST request that queues an app execution job and returns ID of the job
 
 endpoint = /v1/workflows/{appId}/jobs/
 
###x.getJobs(appID)
 GET request that returns the jobs for the given Alteryx Analytics App
 
 endpoint = /v1/workflows/{appId}/jobs/
 
###x.getJobStatus(jobID)
 GET request that requires a jobID input and returns the status of that job
 
 endpoint = /v1/jobs/{jobId}/
 
### x.getJobOutput(jobID, outputID)
 GET request that requires a jobID and an outputID which returns the output for a given job (FileURL) 
 
 endpoint = /v1/jobs/{jobId}/output/{outputId}/
 
### x.getApp(appID) 
 GET request that returns the App that was requested
 
 endpoint = /v1/jobs/{jobId}/output/{outputId}/
 