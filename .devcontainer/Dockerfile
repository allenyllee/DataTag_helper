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
    && apt install -y --install-recommends winehq-devel \
    && apt install --fix-missing -y xvfb \
    && apt install -y binutils libc6

# fix: E: Package 'winetricks' has no installation candidate
# https://www.reddit.com/r/linuxquestions/comments/sr4zmz/comment/in0d7ch/?utm_source=share&utm_medium=web2x&context=3
RUN echo "deb http://deb.debian.org/debian bullseye main contrib non-free" >> /etc/apt/sources.list \
    && apt update && apt install -y winetricks

USER vscode
WORKDIR /home/vscode

# Silence all the "fixme: blah blah blah" messages from wine
# see: https://github.com/benley/docker-wine-python-dotnet/blob/master/Dockerfile
ENV WINEDEBUG fixme-all

# need winetrick to install corefonts to avoid below error
# #9 0.610 0024:fixme:heap:RtlSetHeapInformation 00000000 1 00000000 0 stub
# #9 0.691 0040:err:ole:StdMarshalImpl_MarshalInterface Failed to create ifstub, hr 0x80004002
# #9 0.691 0040:err:ole:CoMarshalInterface Failed to marshal the interface {6d5140c1-7436-11ce-8034-00aa006009fa}, hr 0x80004002
# #9 0.691 0040:err:ole:apartment_get_local_server_stream Failed: 0x80004002
# #9 0.722 0024:fixme:ver:GetCurrentPackageId (0032FE94 00000000): stub
# see: https://askubuntu.com/a/1200679/735872
RUN WINARCH=win64 winetricks \
    corefonts

# [T202710 Xvfb causes _XSERVTransmkdir: ERROR: euid != 0,directory /tmp/.X11-unix will not be created](https://phabricator.wikimedia.org/T202710)
# symptom: "ERROR: euid != 0,directory /tmp/.X11-unix will not be created."
# rootcause: Xvfb / Xserver creates a /tmp/.X11-unix/94 unix socket and ensure the parent directory belong to root.
# solution: By instructing Xvfb to no more listen on a unix socket, it is no more created. That is done by passing `-nolisten unix`
# $ Xvfb :94 -screen 0 1280x1024x24 -ac -nolisten tcp -nolisten unix
##
# if Xvfb shuts down early or fails to clean up after itself, so I like the idea to use `xvfb-run sh -c 'wine <program> && wineserver -w' && rm -f /tmp/.X*-lock`
# https://github.com/Winetricks/winetricks/issues/1525#issuecomment-740497505
RUN wget https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe \
&& xvfb-run --server-num=99 -e /dev/stdout --server-args="-screen 0 1024x768x24 -nolisten unix" \
sh -c 'wine python-3.6.8-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 && wineserver -w' \
&& rm -f /tmp/.X*-lock \
&& rm python-3.6.8-amd64.exe

RUN xvfb-run --server-num=99 -e /dev/stdout --server-args="-screen 0 1024x768x24 -nolisten unix" \
sh -c 'wine pip install wxpython gooey pyinstaller==3.5 && wineserver -w' \
&& rm -f /tmp/.X*-lock

COPY project_requirements.txt /tmp/conda-tmp/
RUN wine pip install -r /tmp/conda-tmp/project_requirements.txt

# set Conda env
COPY --from=Stage1_Conda /opt/conda /opt/conda

# Initialize conda in bash config fiiles:
RUN conda init bash
RUN echo "conda activate AI_Clerk_helper" >> ~/.bashrc

