FROM gcr.io/dataflow-templates-base/python3-template-launcher-base

ARG WORKDIR=/dataflow/template
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

# Install dependencies
RUN pip install -U pip setuptools wheel
RUN pip install apache-beam[gcp]>=2.50.0 requests>=2.31.0 typing-extensions>=4.5.0

# Copy template files
COPY requirements.txt .
COPY setup.py .
COPY pipeline.py .

ENV FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE="${WORKDIR}/requirements.txt"
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="${WORKDIR}/pipeline.py"

RUN pip install -U -r ./requirements.txt 
