FROM python:3.9-slim

WORKDIR /home/appuser

RUN useradd --user-group --system --uid 1000 appuser && \
    chown -R appuser /home/appuser

RUN pip install --no-cache-dir --upgrade pip pipenv

COPY --chown=appuser Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy --dev --ignore-pipfile

RUN rm Pipfile Pipfile.lock

COPY --chown=appuser scripts ./scripts

USER appuser

CMD ./scripts/start-jupyter.sh
