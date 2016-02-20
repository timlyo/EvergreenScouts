# Api Documentation

All routes accept parameters in the form `<route>?parameter=value&parameter2=value2`

parameters are specified below in the form `name=default_value: type`

## Routes

| :-- | :-- | :-- |
| method | route | description
| `GET` | `/api/news` | Get a news article
| `POST` | `/api/news` | Create a new article returns the id
| `POST` | `/api/news/<id>` | Update article details
| `GET` | `/api/program?title&id` | Get a single program
| `POST` | `/api/program/<id>` | Update a news article
| `DELET` | `/api/program/<id>` | Delete a news article
| `GET` | `/api/images/<id>` | Get an image file



###/api/news

Route to search the news, accepts the parameters:

* start: int - record number to start from
* end: int - record number to end at
* all: bool - quick switch to get all