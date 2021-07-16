# https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html
FROM jupyter/scipy-notebook:python-3.9.5

# LXML, html5lib: so we can use read_html from pandas
# parsel, beautifulsoup4: alternatives to parse and read html
RUN conda install --quiet --yes \
    'lxml=4.6.*' \
    'html5lib=1.1' \
    'parsel=1.5.*' \
    'beautifulsoup4=4.9.*' && \
    conda clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
