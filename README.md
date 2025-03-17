# payload-sender

SYNOPSIS Sends the contents of a file to a specified IP address and port using Python.
DESCRIPTION This script reads the contents of a file and sends it over a TCP connection to a specified IP address and port. It handles potential errors and provides basic feedback, including connection failure detection.
PARAMETER Payload The path to the file whose contents will be sent.
PARAMETER IP The IP address to send the data to.
PARAMETER Port The port number to connect to.
Docker-compose example:

########## SERVICES
services:
app:
image: fbeilke/payload-sender:latest
container_name: Payload_Sender
ports:
  - "5001:5001"
volumes:
  - /payloadsender/payloads:/payloads
  - /payloadsender/config:/config
restart: unless-stopped
