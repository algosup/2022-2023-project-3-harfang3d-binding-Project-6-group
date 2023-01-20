#! bin/bash

# run by writing `sh docker.sh`

# * Setup color variables
    # Font colors :
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

    # Bold font colors :
        BLACKBold='\033[1;30m'
        REDBold='\033[1;31m'
        GREENBold='\033[1;32m'
        ORANGEBold='\033[1;33m'
        BLUEBold='\033[1;34m'
        PURPLEBold='\033[1;35m'
        CYANBold='\033[1;36m'
        LIGHTGRAYBold='\033[1;37m'
        DARKGRAYBold='\033[0;30m'
        LIGHTREDBold='\033[0;31m'
        LIGHTGREENBold='\033[0;32m'
        YELLOWBold='\033[0;33m'
        LIGHTBLUEBold='\033[0;34m'
        LIGHTPURPLEBold='\033[0;35m'
        LIGHTCYANBold='\033[0;36m'
        WHITEBold='\033[0;37m'


    # Reset
        NC='\033[0m' # Reset

{
    docker build -t fabgen .
} && {
    echo -e "${GREEN}Docker image built successfully${NC}"
} || {
    echo -e "${REDBold}Docker image build failed, Do you have docker running ?${NC}"
    exit 1
}
echo "To enter the container run :"
echo -e "${GREEN}docker run --name fabgen -it --rm fabgen:latest${NC}"
echo "once inside the container run :"
echo -e "${GREEN}python3 tests.py --linux --rust${NC}"