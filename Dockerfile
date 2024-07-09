FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04 as cuda-base
FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    sudo \
    bzip2 \
    libx11-6 \
    vim \
    build-essential \
    screen \
    unoconv \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get clean autoclean && apt-get autoremove --yes && rm -rf /var/lib/{apt,dpkg,cache,log}/

# CUDA Home
COPY --from=cuda-base /usr/local/cuda /usr/local/cuda
COPY --from=cuda-base /usr/local/cuda-11.8 /usr/local/cuda-11.8
# CUdnn Home
#COPY --from=cuda-base /usr/lib/x86_64-linux-gnu /usr/lib/x86_64-linux-gnu

ENV PATH=/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:/usr/local/cuda-11.8/targets/x86_64-linux/lib:/usr/local/lib/python3.9/site-packages/torch/lib:${LD_LIBRARY_PATH}

COPY . /app

CMD ["bash"]