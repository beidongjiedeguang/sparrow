FROM beidongjiedeguang/pytorch-paddlenlp:cuda11.3-cudnn8-ubuntu2004

RUN sudo apt update && sudo apt install curl -y
RUN curl -sL https://deb.nodesource.com/setup_16.x -o /tmp/nodesource_setup.sh
RUN sudo bash /tmp/nodesource_setup.sh
RUN sudo apt install nodejs -y
RUN sudo npm install -g pnpm

