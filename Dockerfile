# Python version can be changed, e.g.
# FROM python:3.8
# FROM ghcr.io/mamba-org/micromamba:1.5.1-focal-cuda-11.3.1

FROM docker.io/mambaorg/micromamba:1.5.5-bookworm-slim AS micromamba
FROM micromamba AS builder

RUN \
    --mount=type=cache,sharing=private,target=/home/mambauser/.mamba/pkgs,uid=57439,gid=57439 \
    --mount=type=cache,sharing=private,target=/opt/conda/pkgs,uid=57439,gid=57439 \
    micromamba -y -n base install -c conda-forge python=3.12 nibabel=5.2.0 numpy=1.26.3 tqdm=4.66.1

ARG SRCDIR=/home/mambauser/pl-zerobg
RUN mkdir "${SRCDIR}"
WORKDIR ${SRCDIR}

COPY requirements.txt .
ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN pip install -r requirements.txt

COPY . .
RUN pip install . && cd / && rm -rf ${SRCDIR}
WORKDIR /

CMD ["zb"]

LABEL org.opencontainers.image.authors="FNNDSC <dev@babyMRI.org>" \
      org.opencontainers.image.title="Zero MRI Background" \
      org.opencontainers.image.description="Set the background intensity of a MRI to 0"
