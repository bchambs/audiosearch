audiosearch
============

Web app created in Django to be deployed with docker.  Uses Echo Nest API to give music information and suggest similar artists / songs.  Below is my to-do list of features.

1. Develop algorithm to crop artist images so they do not appear stretched.  This will probably be done in javascript.

2. Develop algorithm to return meaningful artist biographies.  Current version is lacking.

3. Replace numbered lists with visually pleasing tables.

4. Add footer div to fill page.

5. Refactor the padding / margins on each page. 

6. I'm tempted to place the bottom nine artists on the trending page in a table in one block.

7. Add hints as title hover-text.  Give these elements dotted underlines.  Example: explain how suggested song list is generated.

8. Find a nice color scheme.

9. Add a template tag to turn rating decimal into a percentage.

10. Rank this list in order of priority. 

11. Change titles to give more information.

12. Combine remove_duplicate_artists and remove_duplicate_songs somehow.

13. Add error checking to all api calls.