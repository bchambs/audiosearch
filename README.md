audiosearch
============

audiosearch is an open source web application created in the Django web framework.  This website acts as an interactive implementation of The Echo Nest's music services.  It uses a python wrapper library (pyechnoest) to abstract the restful service calls into python objects.  

I created this project for two reasons: 

1. I wanted to improve my front-end development.
2. I want to host an open project which can be criticized for its visual design as well as its source code structure.

I am currently developing audiosearch v1.1 which will fix certain defects and add functionality:

1.  COMPLETE: Artists and songs are not being mapped correctly.  Duplicates will always map to the most popular instance of the name. (defect)
2.  Improve python code readability by removing magic numbers, revamp index caching. (defect)
3.  Add pagination to all result pages including the artist and song pages. (functionality)
4.  Increase page movement by adding artist hotlinks next to song names. (functionality)
5.  Various visual enhancements. (functionality)
6.  Rename trending to something else.  Replace featured with new 'trending' which lists the top 10 (?) most search artists (and songs?). (functionality)
7.  Make images appear as modal. (functionality)
8.  Have a changelog modal in the footer of each page. (functionality)
9.	Establish user sessions to track their recent searches.  Display this on a sidebar (?). (functionality)