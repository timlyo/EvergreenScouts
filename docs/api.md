# Api Documentation

All routes accept parameters in the form `<route>?parameter=value&parameter2=value2`

## Routes

###/api/news

Route to search the news, accepts the parameters:

* start: int - record number to start from
* end: int - record number to end at
* all: bool - quick switch to get all
    

###/api/program

Route to get program information

####Get
Return the program

####POST
Update the program

Both methods accept a name parameter to specify which program to update

###/api/images

Route to get images

####Get
Return the image

####Parameters

* id - id of the file to load
* file - image file to load, extension not needed
* date - accepts a single date to load or a range in iso format
* location - not yet implemented