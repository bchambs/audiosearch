audiosearch
============

audiosearch is an open source web application designed to allow users to find new music.  This website is an interactive implementation of The Echo Nest's web services.  


Version 2.0 is in development:
* Implement celery task queue and redis cache to handle async requests. COMPLETE
* Replace 'featured artist' with the top 10 most searched artists / songs on audiosearch.
* Drop pyechonest and create a minimal REST consumption library. COMPLETE
* Redesign templates.
* Add cache clear algorithm. (LRU with fixed size?)
* Add js util to center artist tile images.