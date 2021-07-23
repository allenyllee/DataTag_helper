# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.187.0/containers/python-3-anaconda/.devcontainer/base.Dockerfile

FROM mcr.microsoft.com/vscode/devcontainers/anaconda:0-3

# Copy environment.yml (if found) to a temp location so we update the environment. Also
# copy "noop.txt" so the COPY instruction does not fail if no environment.yml exists.
COPY environment.yml* .devcontainer/noop.txt /tmp/conda-tmp/
RUN if [ -f "/tmp/conda-tmp/environment.yml" ]; then /opt/conda/bin/conda env update -n base -f /tmp/conda-tmp/environment.yml; fi \
    && rm -rf /tmp/conda-tmp

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>


RUN chown 1000:1000 -R /opt/conda/

RUN apt update \
    && apt install -y software-properties-common \
    && dpkg --add-architecture i386 \
    && wget -qO - https://dl.winehq.org/wine-builds/winehq.key | sudo apt-key add - \
    && apt-add-repository https://dl.winehq.org/wine-builds/debian/ \
    && wget -O- -q https://download.opensuse.org/repositories/Emulators:/Wine:/Debian/Debian_10/Release.key | sudo apt-key add - \
    && echo "deb http://download.opensuse.org/repositories/Emulators:/Wine:/Debian/Debian_10 ./" | sudo tee /etc/apt/sources.list.d/wine-obs.list

RUN apt update \
    && apt install -y binutils libc6 \
    && apt install -y --install-recommends winehq-devel \
    && apt install --fix-missing -y xvfb

USER vscode

WORKDIR /home/vscode

RUN conda create --name AI_Clerk_helper python=3.6


# Make RUN commands use the new environment:
SHELL ["conda", "run", "--no-capture-output", "-n", "AI_Clerk_helper", "/bin/bash", "-c"]

COPY project_requirements.txt requirements.txt /tmp/conda-tmp/

RUN conda install wxpython \
    && conda install -c conda-forge gooey \
    && pip3 install -r /tmp/conda-tmp/project_requirements.txt \
    && pip3 install -r /tmp/conda-tmp/requirements.txt \
    && pip3 install pyinstaller==3.5

RUN winecfg \
&& wget https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe \
&& xvfb-run --server-args="-screen 0, 1024x768x24" wine python-3.6.8-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 \
&& rm python-3.6.8-amd64.exe \
&& wine pip install wxpython gooey pyinstaller==3.5 \
&& wine pip install -r /tmp/conda-tmp/project_requirements.txt


# Initialize conda in bash config fiiles:
RUN conda init bash
RUN echo "conda activate AI_Clerk_helper" >> ~/.bashrc

