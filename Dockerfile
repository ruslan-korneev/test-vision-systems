FROM python:3.11-slim as python-base
RUN apt-get update && \
    apt-get install -y build-essential cmake && \
    apt-get install -y libopenblas-dev liblapack-dev && \
    apt-get install -y libx11-dev libgtk-3-dev

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.4.2 \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    DLIB_SHAPE_PREDICTOR="/opt/pysetup/landmarks.dat"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


# `builder-base` stage is used to build deps + create our virtual environment
FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential \
        openssh-client \
        libffi-dev \
        git \
        libpcre3 libpcre3-dev

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python -

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
COPY src ./src/
COPY README.md ./
# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --only main

# install shape predictor model
RUN curl -o landmarks.dat.bz2 http://dlib.net/files/shape_predictor_5_face_landmarks.dat.bz2
RUN bzip2 -d landmarks.dat.bz2

# `development` image is used during development / testing
FROM python-base as development
WORKDIR $PYSETUP_PATH

# copy in our built poetry + venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
#COPY --from=builder-base $DLIB_SHAPE_PREDICTOR $DLIB_SHAPE_PREDICTOR

# quicker install as runtime deps are already installed
RUN poetry install --no-root

FROM python-base as production

WORKDIR /app
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
#COPY --from=builder-base $DLIB_SHAPE_PREDICTOR $DLIB_SHAPE_PREDICTOR
COPY entrypoint.sh .

# Create user so we don't run docker as root
RUN groupadd -r flask && useradd -r -u 999 -g flask flask

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "src.app:app", \
    "-w", "4", \
    "-b", "0.0.0.0:5000", \
    "--error-logfile", "-", \
    "--enable-stdio-inheritance", \
    "--log-level", "debug"]
