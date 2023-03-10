# linux image with golang, python and lua
FROM ubuntu:latest



# install golang
RUN apt-get update && apt-get install -y golang
# install apt-get -y install golang-golang-x-tools
RUN apt-get install -y golang-golang-x-tools
# install curl
RUN apt-get install -y curl
# install python
RUN apt-get install -y python3
# install pip
RUN apt-get install -y python3-pip

# pip install pypeg2
RUN pip3 install pypeg2
# install lua
RUN apt-get install -y lua5.2
# install cmake
RUN apt-get install -y cmake
# install libclang
RUN apt-get install -y libclang-dev

# Get Rust
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

COPY . ./app/
WORKDIR /app

# CMD ["/bin/bash"]