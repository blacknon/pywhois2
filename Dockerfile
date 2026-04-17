ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml setup.py README.md LICENSE ./
COPY pywhois2 ./pywhois2
COPY scripts ./scripts
COPY tests ./tests
COPY TEMPLATE_COVERAGE.md ./TEMPLATE_COVERAGE.md
COPY .github/scripts/run_ci.sh /usr/local/bin/run_ci.sh

RUN python -m pip install --upgrade pip \
    && python -m pip install . \
    && chmod +x /usr/local/bin/run_ci.sh

CMD ["sh", "/usr/local/bin/run_ci.sh"]
