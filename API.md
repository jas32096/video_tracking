## This api is self documenting, with [JSON Hyper-Schema](http://json-schema.org/latest/json-schema-hypermedia.html).

See `/schema` for indepth technicals.

```javascript
{
    "$schema": "http://json-schema.org/draft-04/hyper-schema#",
    "properties": {
        "videos": {
            "$ref": "/videos/schema#"
        },
        "views": {
            "$ref": "/views/schema#"
        }
    }
}
```
# For usage examples please see [Flask-Potion](http://potion.readthedocs.io/en/latest/quickstart.html).

--------------------------------------------------------------------------------
## Videos `/videos`
```javascript
{
    "$uri": "/videos/4",
    "brand": "Brandy Brand",
    "count": 3,
    "created_at": "2017-08-14T02:23:04.415046",
    "name": "test",
    "published": "2017-08-13",
    "updated_at": "2017-08-14T02:23:04.415054"
}
```
- Retrive **GET** `/videos/<id>`
- Create **POST** `/videos`
    - name: `str`
    - brand: `str`
    - published: `date`
        - isoformat i.e `'2017-08-13'`
- Update **PATCH** `/videos/<id>`
- Delete **DELETE** `/videos/<id>`
    - When a video is deleted, all related views are deleted, too.
- Add View **POST** `/videos/<id>/add_view`
    - Create view and add it to this video's views
        - Same effect as **POST** to `/views` with `{"video": <id>}`
    - response json
        - count: `int`
            - The new video count
        - view: `View`
- Get view count after a certain date **GET** `/videos/<id>/view_count`
    - args
        - date: `str`
    - response: `int`
    - This is a convience endpoint. You can get more functionality out of [filters](http://potion.readthedocs.io/en/latest/quickstart.html#filtering-sorting).
    
    ```bash
    jacobschechter ~> http -h HEAD :5000/views \
                       where=='{"video": 4, "created_at": {"$gte": "2017-08-05T00:00:00Z"}}' | \
                       grep '^X-Total-Count:' | cut -f2 -d' '
    5
    ```

## Views `/views`
```javascript
{
    "$uri": "/views/45",
    "created_at": "2017-08-14T03:49:21.823187",
    "ip": "127.0.0.1",
    "updated_at": "2017-08-14T03:49:21.823193",
    "user_agent": "HTTPie/0.9.9",
    "video": {
        "$ref": "/videos/4"
    }
}
``` 
- Create **POST** `/views`
    - video: `ToOne(Video)`
        - Either the id as an `int` or a `$ref` in the form `{"$ref": "/videos/<id>"}`

--------------------------------------------------------------------------------
# Other Examples
### Get all total views of a particular brand
```bash
jacobschechter ~> http :5000/videos where=='{"brand": "Brandy Brand"}' | jq .[].count | paste -sd+ - | bc
7
```