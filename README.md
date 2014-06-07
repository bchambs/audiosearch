audiosearch
============

audiosearch is an open source web application created in the Django web framework.  This website acts as an interactive implementation of The Echo Nest's music services.  I am using the pyechnoest library to abstract these services to python objects.

I made this to experiment with css / javascript / django.  

Version 2.0 is in development:
* Complete redesign of every template.
* Replace featured artist page with trending system to track popular music queries (not Echo Nest).
* Add page caching.
* Refactor css and javascript source files into groups.
* Refactor views.py to be more readable.

Planned features not included in v2.0:
* Design an ajax or django handler for EchoNestAPIError exceptions.  Currently, django serves a 500 page if a user requests music data and my key has exceeded its access limit.  Implement a handler to load the page and serve (load) the music data when accesses are available.