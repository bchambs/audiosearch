audiosearch
============

audiosearch is an open source web application created in the Django web framework.  This website acts as an interactive implementation of The Echo Nest's web services.  I am using the pyechonest library to abstract these services to python objects.

Version 2.0 is in development:
* Implement celery task queue and redis cache to handle async requests. 
* Replace 'featured artist' with the top 10 most searched artists / songs on audiosearch.
* Drop pyechonest and create a minimal REST consumption library.
* Redesign templates.
