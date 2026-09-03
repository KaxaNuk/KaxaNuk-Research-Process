# KN Research Process dev container: JupyterLab, with the project on Python 3.14.
#
# Two interpreters live here on purpose:
#   - the base image's Python 3.13 ($CONDA_DIR) runs the Jupyter *server*;
#   - a uv-managed Python 3.14 (/opt/venv) runs the *notebooks*, registered as
#     a kernel below.
# The split exists because pyproject.toml declares requires-python >= 3.14 and
# quay.io/jupyter/minimal-notebook has no python-3.14 tag (it tops out at
# 3.13.15). Installing the project into $CONDA_DIR the way a >=3.12 project
# could would simply fail at `uv sync`.

FROM quay.io/jupyter/minimal-notebook:python-3.13
ENV GRANT_SUDO='yes'

# Root-only setup: apt packages, plus the two dirs uv writes to outside $HOME
# so they survive a mounted home and stay out of the bind-mounted /workspace.
# rsync is used by the devcontainer lifecycle hooks to populate cache volumes.
USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends rsync \
    && rm -rf /var/lib/apt/lists/* \
    && install -d -o $NB_UID -g users /opt/venv /opt/uv-python \
;
USER $NB_UID

WORKDIR /workspace
COPY --chown=$NB_UID:users . /workspace

RUN pip install --upgrade \
    pip \
    uv \
;

# The project environment, deliberately outside /workspace: the devcontainer
# bind-mounts the repo over that path at runtime, which would shadow anything
# installed into it during the build.
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
ENV UV_PYTHON_INSTALL_DIR=/opt/uv-python

# --frozen installs exactly what uv.lock pins, so the container matches the
# local .venv instead of silently resolving newer versions at build time.
RUN uv python install 3.14 \
    && uv sync --all-groups --frozen \
;

# Register /opt/venv as a kernel under $CONDA_DIR rather than the venv's own
# prefix -- the Jupyter server runs from $CONDA_DIR and only discovers kernels
# on its own search path.
RUN /opt/venv/bin/python -m ipykernel install \
        --prefix="${CONDA_DIR}" \
        --name kn-research-process \
        --display-name "KN Research Process (Python 3.14)" \
;
