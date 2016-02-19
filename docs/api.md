# Api Documentation

All routes accept parameters in the form `<route>?parameter=value&parameter2=value2`

parameters are specified below in the form `name=default_value: type`

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

Route to get images. doesn't handle sorting, items are returned in the order that they are in the database.

####Get
Returns a json list of images. If no parameter are specified then the most recent images are returned

####Parameters

* id: int - comma separated ids of the files to load 
* file: string - comma separated files image file to load, extension not needed(always jpg)
* date: string - accepts a single date to load or a range in iso format
* location - not yet implemented
* limit=50: int - maximum number of images to be loaded 