# audio-podcast
Programmatically create an audio podcast using Python and ElevenLabs

There are a couple of prerequisites. As this process uses ElevenLabs for its API,
you need to sign up for a paid plan. At the time of writing, this can be as low as $5 per month, which  
gets you 30 or 60 minutes of podcast per month, depending on the quality of the voices used. You can check that out using 
the link below. This is an affiliate link; if you sign up using it, I receive a small commission.

https://try.elevenlabs.io/ss0de8fi4xhm

A comprehensive description of the process of creating an audio-only podcast, from start to finish, can be found on the 
Level Up Coding blog. The link to that is below. 

https://medium.com/gitconnected/programmatically-create-an-audio-podcast-5934bdd3ae98

But briefly, the steps are:

1) Create a new development environment using the tool of your choice (I use miniconda) and activate it.
2) Install the libraries from the requirements.txt file
3) Sign up to ElevenLabs if required and create or choose two voices as your podcast hosts - note their IDs. Also, generate an API key
4) Download the ffmpeg.exe file from https://www.gyan.dev/ffmpeg/builds/
5) Add the ElevenLabs API key from step (3) to your environment, and add the folder where your ffmpeg.exe file lives to your PATH variable
6) Create the text that your podcast hosts will speak (see the podcast_example_text.json for how this should be formatted)
7) Run the code to create the podcast e.g

  python podcast.py --input_file podcast_example_text.json --output_file podcast.mp3 --tts_service elevenlabs

  Happy podcasting!
