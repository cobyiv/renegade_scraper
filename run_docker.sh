#!/bin/bash

#re-build
sudo docker build -t renegade-scraper .

#run in the background
sudo docker run -d renegade-scraper:latest


#OLD
#docker run -it --rm -v "$(pwd)":/app renegade-scraper