# pyModularJSON

Allows recursive loading of JSON files. 


Authored by Edwin Peters
## Install
`setup.py install`

## Usage

base.json:
```
// comments
{
    "param2a": 2,
    "nestedParam2a":{
	"a": "notaNumber",
	"c": "set by base"
    }
}
```

main.json:
```
// comments
{
    "configBase": ["base.json"], // parent config file name relative to this file
    "param1": 4,
    "nestedParam1":{
	"a":39,
	"b":["peee","e","new"],
	"c": "set by main"
    } 
}
```

In Python:
```
from pyLoadModularJson import loadModularJson

cfg = loadModularJson('base.json')

print(cfg)

```

Child files will overwrite attributes from base files.


See more examples in `tests`
