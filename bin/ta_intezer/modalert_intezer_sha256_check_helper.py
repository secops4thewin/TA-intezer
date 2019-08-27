
# encoding = utf-8

def process_event(helper, *args, **kwargs):
    """
    # IMPORTANT
    # Do not remove the anchor macro:start and macro:end lines.
    # These lines are used to generate sample code. If they are
    # removed, the sample code will not be updated when configurations
    # are updated.

    [sample_code_macro:start]

    # The following example gets the setup parameters and prints them to the log
    api_key = helper.get_global_setting("api_key")
    helper.log_info("api_key={}".format(api_key))
    index = helper.get_global_setting("index")
    helper.log_info("index={}".format(index))

    # The following example sends rest requests to some endpoint
    # response is a response object in python requests library
    response = helper.send_http_request("http://www.splunk.com", "GET", parameters=None,
                                        payload=None, headers=None, cookies=None, verify=True, cert=None, timeout=None, use_proxy=True)
    # get the response headers
    r_headers = response.headers
    # get the response body as text
    r_text = response.text
    # get response body as json. If the body text is not a json string, raise a ValueError
    r_json = response.json()
    # get response cookies
    r_cookies = response.cookies
    # get redirect history
    historical_responses = response.history
    # get response status code
    r_status = response.status_code
    # check the response status, if the status is not sucessful, raise requests.HTTPError
    response.raise_for_status()


    # The following example gets the alert action parameters and prints them to the log
    sha_256_hash = helper.get_param("sha_256_hash")
    helper.log_info("sha_256_hash={}".format(sha_256_hash))

    search_description = helper.get_param("search_description")
    helper.log_info("search_description={}".format(search_description))


    # The following example adds two sample events ("hello", "world")
    # and writes them to Splunk
    # NOTE: Call helper.writeevents() only once after all events
    # have been added
    helper.addevent("hello", sourcetype="sample_sourcetype")
    helper.addevent("world", sourcetype="sample_sourcetype")
    helper.writeevents(index="summary", host="localhost", source="localhost")

    # The following example gets the events that trigger the alert
    events = helper.get_events()
    for event in events:
        helper.log_info("event={}".format(event))

    # helper.settings is a dict that includes environment configuration
    # Example usage: helper.settings["server_uri"]
    helper.log_info("server_uri={}".format(helper.settings["server_uri"]))
    [sample_code_macro:end]
    """
    import json
    import time
    
    helper.log_info("Alert action intezer_sha256_check started.")

    # TODO: Implement your alert action logic here
    proxy = helper.get_proxy()
    
    if proxy:
        use_proxy = True
    else:
        use_proxy = False
    
    #Get Global Parameters
    api_key = helper.get_global_setting("api_key")
    index_name = helper.get_global_setting("index")
    
    #Get Local Parameters
    sha_256_hash = helper.get_param("sha_256_hash")
    search_description = helper.get_param("search_description")
    
    #Create the URI String that looks for the domain
    url = 'https://analyze.intezer.com/api/v1-2/analyze-by-sha256'
    
    method = "POST"
    
    if api_key:
        helper.log_info("intezer_sha256_check Action - API key exists.")
        params = {
            'sha256' : sha_256_hash,
            'api_key' : api_key
            }
    else:
        helper.log_info("intezer_sha256_check Action - API key does not exist.")
        params = {
            'sha256' : sha_256_hash
            }  
    
     #Make Initial HTTP Request
    response = helper.send_http_request(url, method, parameters=None, payload=params, headers=None, cookies=None, verify=True, cert=None, timeout=10, use_proxy=use_proxy)
    
    json_load = response.json()
    
    if response.status_code == 201:
        #If the request is successfull grab the API Keys
        if api_key:
            params = {
                'api_key' : api_key
                }
        #Grab the result URL from the response
        result_url = 'https://analyze.intezer.com/api' + str(json_load['result_url'])
        
        #Pause 10 Seconds While Analysing
        time.sleep(10)
        #Issue a new request to the new URL.
        result_response = helper.send_http_request(result_url, method, parameters=None, payload=params, headers=None, cookies=None, verify=True, cert=None, timeout=10, use_proxy=use_proxy)
        
        #Create a 0 number for incrementing a sleep counter
        i = 0
        
        #While the result is not succeeded or 50 seconds has not elapsed
        while i<10 and result_response.json()['status'] != 'succeeded' :
            #Sleep 5 seconds
            time.sleep(5)
            
            #Log a pause in the events
            helper.log_info("intezer_sha256_check Action - Sleeping 5 seconds whilst waiting for data to return")
            
            #Issue a new response
            result_response = helper.send_http_request(result_url, method, parameters=None, payload=params, headers=None, cookies=None, verify=True, cert=None, timeout=10, use_proxy=use_proxy)
            
            #Increment the counter
            i+=1
            if i == 10:
                helper.log_error("intezer_sha256_check Action - Analysis of event took longer than 50 seconds")
        
        json_load = result_response.json()
        json_load['search_description'] = search_description
        json_load['search_type'] = "Intezer API Lookup - SHA 256"
        
        #Convert output to JSON String
        json_data = json.dumps(json_load)
        
        #Add Event to Adaptive Response Framework
        helper.addevent(json_data, sourcetype="intezer:json")
        try:
            #Try writing to the specified index in global settings
            helper.writeevents(source="intezer", index=index_name, host="adaptive_response")
        except Exception as e:
            #If that fails write this as an exception
            helper.log_error("Error with writing event. Error Message:{}".format(e))

        
    else:
        helper.log_error("Error with writing event. Error Message:{}".format(response.json()))
    
    
    return 0
