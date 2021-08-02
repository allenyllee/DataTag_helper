# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.187.0/containers/python-3-anaconda/.devcontainer/base.Dockerfile

FROM mcr.microsoft.com/vscode/devcontainers/anaconda:0-3 AS Stage1_Conda

# Copy environment.yml (if found) to a temp location so we update the environment. Also
# copy "noop.txt" so the COPY instruction does not fail if no environment.yml exists.
COPY environment.yml* .devcontainer/noop.txt /tmp/conda-tmp/
RUN if [ -f "/tmp/conda-tmp/environment.yml" ]; then /opt/conda/bin/conda env update -n base -f /tmp/conda-tmp/environment.yml; fi \
    && rm -rf /tmp/conda-tmp

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

RUN chown 1000:1000 -R /opt/conda/

USER vscode
WORKDIR /home/vscode

RUN conda create --name AI_Clerk_helper python=3.6

# Make RUN commands use the new environment:
SHELL ["conda", "run", "--no-capture-output", "-n", "AI_Clerk_helper", "/bin/bash", "-c"]

RUN conda install wxpython \
    && conda install -c conda-forge gooey \
    && pip3 install pyinstaller==3.5

COPY project_requirements.txt /tmp/conda-tmp/
RUN pip3 install -r /tmp/conda-tmp/project_requirements.txt

COPY requirements.txt /tmp/conda-tmp/
RUN pip3 install -r /tmp/conda-tmp/requirements.txt

########### Stage2 ###########
FROM mcr.microsoft.com/vscode/devcontainers/anaconda:0-3 AS Stage2_Wine

# Copy environment.yml (if found) to a temp location so we update the environment. Also
# copy "noop.txt" so the COPY instruction does not fail if no environment.yml exists.
COPY environment.yml* .devcontainer/noop.txt /tmp/conda-tmp/
RUN if [ -f "/tmp/conda-tmp/environment.yml" ]; then /opt/conda/bin/conda env update -n base -f /tmp/conda-tmp/environment.yml; fi \
    && rm -rf /tmp/conda-tmp

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

RUN apt update \
    && apt install -y software-properties-common \
    && dpkg --add-architecture i386 \
    && wget -qO - https://dl.winehq.org/wine-builds/winehq.key | sudo apt-key add - \
    && apt-add-repository https://dl.winehq.org/wine-builds/debian/ \
    && wget -O- -q https://download.opensuse.org/repositories/Emulators:/Wine:/Debian/Debian_10/Release.key | sudo apt-key add - \
    && echo "deb http://download.opensuse.org/repositories/Emulators:/Wine:/Debian/Debian_10 ./" | sudo tee /etc/apt/sources.list.d/wine-obs.list \
    && apt update \
    && apt install -y --install-recommends winehq-devel winetricks \
    && apt install --fix-missing -y xvfb \
    && apt install -y binutils libc6

USER vscode
WORKDIR /home/vscode

RUN wget https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe

RUN WINEPREFIX=~/.wine64 WINARCH=win64 winetricks \
    corefonts \
    win10

RUN xvfb-run --server-num=99 -e /dev/stdout --server-args="-screen 0 1024x768x24 -nolisten unix" WINEPREFIX=~/.wine64 wine python-3.6.8-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
# RUN xvfb-run --server-num=99 -e /dev/stdout --server-args="-screen 0 1024x768x24 -ac -nolisten tcp -nolisten unix" wine python-3.6.8-amd64.exe /quiet InstallAllUsers=1 PrependPath=1

RUN rm python-3.6.8-amd64.exe

RUN wine pip install wxpython gooey pyinstaller==3.5

COPY project_requirements.txt /tmp/conda-tmp/
RUN wine pip install -r /tmp/conda-tmp/project_requirements.txt

# set Conda env
COPY --from=Stage1_Conda /opt/conda /opt/conda

# Initialize conda in bash config fiiles:
RUN conda init bash
RUN echo "conda activate AI_Clerk_helper" >> ~/.bashrc

