# web_archive_get

a tool to find archived web pages from different websites using multiple different services. the currently three functions implemented and that are:

## list_page 
get a pages of the url
* url -  the url of the page
RETURN a list of requestable object
## list_subdoamin
get all subdoamin of a domain your looking up
* url -  the url of the domain
RETURN a list of requestable object
## search_url_host
look up website with the same host
* url -  the url of the host
RETURN a list of requestable object
## search_url_subpath
get the all subpath  of the url
* url -  the url of the subpath
RETURN a list of requestable object

# requestable object
## request()
## get_length()
## get_statuscode()
## get_mimetype()
## get_url()