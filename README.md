# ClipperCard Usage API

Clipper Card is the Bay Area transit card. There's no good API for pulling Clipper usage, so I've created a hackish one that uses Selenium. This interacts with the ClipperCard website to retrieve user transit usage data. It automatically logs in to the website, downloads the ride history, and converts it into an JSON record based format for clients to use.

## Application Structure

- A Flask server that handles POST requests at `/get_clipper_usage` endpoint.
- A Selenium script that automates the browser to login and retrieve ride history data from the ClipperCard website.
- A Camelot script to read the downloaded PDF file and parse the data into a pandas DataFrame.

## Prerequisites

The application requires the following dependencies:

- Python 3
- Flask
- Selenium
- Camelot
- Ghostscript
- Tcl-tk

You can install Python dependencies using pip:
```
pip install flask selenium camelot-py[base]
```

Ghostscript and Tcl-tk can be installed on MacOS using brew:
```
brew install ghostscript tcl-tk
```

or on Ubuntu:
```
apt install ghostscript python3-tk
```


You'll also need Firefox and its corresponding Geckodriver installed.

## Running the Server

Run the server using the command:
```
python routes.py
```

Once the server is running, you can send a GET request to `localhost:5000/get_clipper_usage` with your Clipper email and password that you would use to log into Clipper [here](https://www.clippercard.com/ClipperWeb/login.html) in the request body to retrieve the ClipperCard usage data. 

```
curl -X GET -H "Content-Type: application/json" -d '{"email":"myEmail@gmail.com","password":"foobarbaz"}' http://localhost:5000/get_clipper_usage
```

## Notes

Please be aware that the route only currently retrieves Clipper usage data for the most recently used card.