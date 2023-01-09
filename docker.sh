#! bin/bash

# run by writing `sh docker.sh`

# * Setup color variables
    BLACK='\033[0;30m'
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    ORANGE='\033[0;33m'
    BLUE='\033[0;34m'
    PURPLE='\033[0;35m'
    CYAN='\033[0;36m'
    LIGHTGRAY='\033[0;37m'
    DARKGRAY='\033[1;30m'
    LIGHTRED='\033[1;31m'
    LIGHTGREEN='\033[1;32m'
    YELLOW='\033[1;33m'
    LIGHTBLUE='\033[1;34m'
    LIGHTPURPLE='\033[1;35m'
    LIGHTCYAN='\033[1;36m'
    WHITE='\033[1;37m'
    NC='\033[0m' # No Color

docker build -t fabgen .
echo "To enter the container run :"
echo -e "${GREEN}docker run --name fabgen -it --rm fabgen:latest${NC}"
echo "once inside the container run :"
echo -e "${GREEN}python3 tests.py --linux --rust${NC}"