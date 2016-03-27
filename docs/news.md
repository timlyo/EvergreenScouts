This document details everything concerning articles and news.

# Article

``` json
Article{
   create: Date
   updated: Date | None
   title: string
   body: html string
   outline: string
   unit: string
   state: string
}
```

# State

An article can be in a set of states.

*Editing* An article that has just been created an has not yet been finished
*Published* A finished article

# Routes

| :-- | :-- |
| `/news` | Display a list of all news |
| `/news/<id>` | Display a single news article |
| `/news/<id>/edit` | Display the ui for editing a news article |

# Methods

## Create
Ajax POST to `/api/news`. This returns the id of the article that is created. The user is then redirected to the edit page for the created post.

The create button should grey out while the article is being created.

Admin only.

## Read
Ajax GET to `/api/news`. 

## Update
Ajax POST to `/api/news/<id>`. This will update the database with any data that is sent through, and leave the fields that aren't specified in the POST.

The Save button should grey out while the request is processing.

## Delete
Ajax DELETE to `/api/news/<id>`.

Does not delete the article from disk, it can be restored at a later date from the admin panel.

