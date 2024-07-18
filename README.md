# sand-spoon-element-api
Web server and free API that uses OpenAI to generate falling sand elements (for the game [sand-spoon](https://github.com/kiwijuice56/sand-spoon)) from text. 

## Usage
Request from the URL `https://122412240.xyz/?element_name={your_element_name_here}`, replacing `your_element_name_here` with any 12 character word. 
The response will be a JSON file containing a guess at what properties suit that element, such as `color` and `temperature`. 
Requests are limited to 10 per minute from a single IP address to reduce spam.
Requests that violate OpenAI content policy (hate, violence, etc.) will return an empty JSON file.

## Structure
The API code uses Gunicorn and Flask to listen to requests. The server uses Nginx as a reverse proxy and is hosted on a DigitalOcean droplet.
