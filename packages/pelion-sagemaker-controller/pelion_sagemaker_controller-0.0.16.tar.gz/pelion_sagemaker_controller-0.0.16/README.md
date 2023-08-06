## Sagemaker Edge Agent Controller client API for Pelion Edge 

#### PyPi:  [https://pypi.org/project/pelion\_sagemaker\_controller/](https://pypi.org/project/pelion\_sagemaker\_controller/)

This python package simplifies the Data Scientist's job of accessing, via a Sagemaker Jupyter Notebook, the Sagemaker Edge Agent running on their Pelion Edge enabled gateway.

### Controller API Instance Creation

To create an instance of this API:
	
	# Required import
	from pelion_sagemaker_controller import pelion_sagemaker_controller
	
	#
	# Invoke constructor with Pelion API Key, Pelion GW Device ID
	# You can also optionally specify the Pelion API endpoint you want to use
	#
	api = pelion_sagemaker_controller.ControllerAPI(
			api_key='<ak_xxxx>', 
			device_id='<pelion_gw_device_id>', 
			api_endpoint='api.us-east-1.mbedcloud.com'
			)
		
		
### Supported Commands

The following commands are supported by this API:

#### Get Configuration

	api.pelion_get_config()
	
	This call returns a JSON with the current Edge Device representing the 
	Sagemaker service's configuration
	
#### Set Configuration

	api.pelion_set_config({'foo':'bar'})
	
	This call updates or adds key/values to the current Edge Device's configuration
	
#### List Models

	api.pelion_list_models()
	
	This call returns a JSON outlining all of the loaded models
	
#### Load Model

	api.pelion_load_model('model-name','compiled-model-x.y.tar.gz')
	
	This call loads up the requested Sagemaker-compiled model whose compiled 
	contents are located within the S3 bucket defined in the configuration
	and utilized by the Sagemaker service
	
#### Unload Model

	api.pelion_unload_model('model-name')
	
	This call unloads the loaded model referenced by the name 'model-name'
	
#### Reload Model

	api.pelion_reload_model('model-name','compiled-model-x.y.tar.gz')
	
	This call is a convenience method for simply performing an "unload" followed by
	a "load" of a given model using the methods above. 
	
#### Predict

	api.pelion_predict(
	          'model-name',
	          's3:///input.data', 
	          's3:///prediction_result.data'
	          )
	
	This call invokes the model prediction using the specified input.data file that is
	configured to be pulled from the Sagemaker S3 bucket (per configuration). The output
	result from the prediction will be stored in a file that will be saved to the same
	directory in the S3 bucket. 
	
	In addition to S3 bucket support, you can locally reference input/output requirements
	using the "file:///" protocol - in this case the Sagemaker Edge Agent working directory
	on the Pelion Edge Gateway will contain the specified files. 
	
#### Last Command Result

	api.pelion_last_cmd_result()
	
	This call returns the last invocation/call results. In cases where predictions take
	a long time to complete, this call may be used in a polling situation to determine
	when the prediction operation has completed. 

