# Homework 3: Satellite/Aerial Image Retrieval

Make sure that you are working on a vagrant box or a system with OpenCV bindings installed for Python3.

## Installing Dependencies

Python

```bash
$ workon cv
(cv) $ pip install -r requirements.txt
```

## Usage

### Instructions

`cli.py` is the main entry point.

```bash
usage: cli.py [-h] lat1 lon1 lat2 lon2 output

positional arguments:
  lat1        Latitude of the southwest point
  lon1        Longitude of the southwest point
  lat2        Latitude of the northeast point
  lon2        Longitude of the northeast point
  output      Path to the output file

optional arguments:
  -h, --help  show this help message and exit
```

### Example

The following command will create an aerial image of the [Hermann Hall](https://web.iit.edu/event-services/meeting-spaces/hermann-hall-conference-center)

```bash
$ workon cv
(cv) $ python cli.py 41.835095 -87.628891 41.836216 -87.627802 hermann-hall.jpg
```
