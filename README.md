# Track IP

An AppEngine web app, for tracking dynamic IP changes.

## Step 1

Starting from simple *hello world* app.
Defined app in app.yaml file.
Testen on localhost using latest appengine sdk for python.

Started app via:
```sh
user@projectdir$ dev_appserver.py .
```

[our app on port 8080](http://localhost:8080/)
[appengine console on port 8000](http://localhost:8000/)

## Step 2

Renamed helloworld.py to trackip.py
Added SaveIpPage
Added registered application in in app.yaml
[Tested on localhost](http://localhost:8080/ip/save/myhostname/123-secrt-code-xyz)
deployed to appengine via:
```sh
user@projectdir$ appcfg.py update .
```
[Tested on localhost](http://track-ip.appspot.com/ip/save/myhostname/123-secrt-code-xyz)
Added Makefile with runserver and deploy targets.
Added Handler to show IP when GET [whatever.track-ip.appspot.com](http://whatever.track-ip.appspot.com/)

## Step 3

Monitor deployed app on [develoepr console](https://console.developers.google.com/project/track-ip/)
Define data model for storing ip and hostname (kind: Host).
Update save handler to create or update host ip in datastore.
Update show handler to resolve ip based on datastore.

## Step 4

Added Profile kind with reference to user object as a key and list of host keys.
Added login/logout on main page handler.
Creating profile for logged user and loading profile for user with profile already created.
Allow new host cration only for logger users and bind host to user profile.
List user owned hosts on main page.
