FROM nikolaik/python-nodejs:python3.9-nodejs16-slim

WORKDIR /home/appuser

RUN useradd --user-group --system --uid 1000 appuser && \
    chown -R appuser /home/appuser

RUN pip install --no-cache-dir --upgrade pip pipenv

COPY --chown=appuser Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy --dev --ignore-pipfile

# https://github.com/mwouts/jupytext#install
RUN jupyter labextension install jupyterlab-jupytext

RUN rm Pipfile Pipfile.lock

COPY --chown=appuser scripts ./scripts
COPY --chown=appuser pyfriends ./pyfriends

USER appuser

CMD ./scripts/start-jupyter.sh
