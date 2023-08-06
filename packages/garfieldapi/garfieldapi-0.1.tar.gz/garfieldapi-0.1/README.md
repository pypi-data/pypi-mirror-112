# garfieldapi

[![](https://shields.io/badge/pypi-0.1-blue?style=flat&logo=pypi)](https://pypi.org/project/listevery)
[![](https://shields.io/badge/made%20with-python-lightgray?style=flat&logo=python)](https://python.org/downloads)

<img src="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/1ffb340c-45b5-4137-8b12-98f2fe9645c6/de2cmeb-139ed35f-14f2-486c-9b22-187c2b5e4db7.png/v1/fill/w_800,h_1247,strp/garfield__png__by_autism79_de2cmeb-fullview.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MTI0NyIsInBhdGgiOiJcL2ZcLzFmZmIzNDBjLTQ1YjUtNDEzNy04YjEyLTk4ZjJmZTk2NDVjNlwvZGUyY21lYi0xMzllZDM1Zi0xNGYyLTQ4NmMtOWIyMi0xODdjMmI1ZTRkYjcucG5nIiwid2lkdGgiOiI8PTgwMCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.bcj0y84uy6AY1LED4YismeX84w9xV2ORZzSKrNROFxw" height=60>

> Yet another Garfield comic finder!

## Usage
This package supports image downloading and comic link finding for Garfield comics. Huge thanks to [ermel.org](https://ermel.org/garfield.php) for providing all the comics made to this day. 

`garfieldapi can be run from the command-line and in a python file!`

Command line:
```
>> import garfieldapi
>> garfieldapi.getlnk('19-06-1978') # dd-mm-yyyy format
'http://images.ucomics.com/comics/ga/1978/ga780619.gif'
>> import os
>> garfieldapi.getimg('12-07-2021', os.getcwd(), 'comic') # date, location, filename
>>
```

Python file (pretty similar):
```
# This is an example
import garfieldapi
import os
print('Downloading comic from src: '+garfieldapi.getlnk('19-06-1978')+'...')
garfieldapi.getimg('19-06-1978', os.getcwd(), 'comic')
```

So try everything out!