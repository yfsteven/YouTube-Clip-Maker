# YouTube-Clip-Maker

Thanks to lemnoslife, transcibe-anything

For now, it works on terminal or interactive shell. 

Nothing was verified about the ~~proper resize~~ or subtitles. 

Maybe, the subtitle is working, but probably does not fit inside of the screen.


[Simple YouTube API](https://github.com/jonnekaunisto/simple-youtube-api)

Documentation is hard to read, especially the API key and credential part. I will put my own explanation.

1. Go to console.cloud.google.com
2. Set up Project
3. Enable YouTube Data API V3
4. Go to the credentials section of APIs & Services on the left
5. On top, it should say "+ CREATE CREDENTIALS".
6. Click on OAuth client ID
7. Choose "Desktop app" for application type and finish it
8. Once done, download the JSON file and rename it to client_secret.json
9. Make sure to add your own account as a Test User on OAuth consent screen
10. Follow the documentation of Simple YouTube API
11. The second file path, you just need to make a file yourself-> "channel.login("client_secret.json", "credentials.storage")"
12. If it goes well, when you run the program, it should open up a link to login your account and ask for permissions
