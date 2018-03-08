# Intezer Add-On for Splunk

## Intezer About
Intezer has developed novel technology- the only solutions to apply biological immune system concepts to cyber security. Through its ‘DNA mapping’ approach to code, Intezer provides enterprises with unparalleled threat detection that accelerates incident response and eliminates false positives, while protecting against fileless malware, APTs, code tampering and vulnerable software.

## Overview
This Add-On provides a method to use Splunk Adaptive Response to automate lookup of a SHA26 hash against the Intezer

## Intezer Add-On For Splunk Requirements
This Add-On requires access to the Intezer API located [here](http://www.intezer.com/intezer-analyze/) and the Splunk Common Information Model App located [here](https://splunkbase.splunk.com/app/1621/)
If you are a community user please contact support@intezer.com to get access to an API key.


### Installation
1. Either git clone this directory 'git clone https://github.com/secops4thewin/TA-intezer.git' or download the spl file located here.
2. Install the add-on to the indexer and search head in your Splunk environment
3. On the Search Head open the add on by going to http://yoursplunkserver:8000/en-GB/app/TA-intezer/configuration
4. Enable a proxy if it is required
5. Click Add-on Settings and enter the API Key and the Index. 
6. Click Save
7. If you have proxy rules please allow https://analyze.intezer.com/api and from your Search Head
8. Create a search that produces a result such as a sha256 hash and pass the results using the Splunk tokens such as $result.sha256$


## Release Notes
0.0.1 Initial release with API functionality