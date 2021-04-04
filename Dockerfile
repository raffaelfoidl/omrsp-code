# A version with a newer micro version (e. g. 3.7.11) could also be used as micro versions
# generally only consist of bugfixes and do not introduce incompatibilities. As of writing
# this experiment, 3.7.10 is the most recent Python 3.7 version.
FROM python:3.7.10-slim

WORKDIR /home

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

# Ignore errors during installation of documentation dependencies with "exit 0" since they
# are not strictly required to execute the script and should not make the image build fail.
COPY requirements-doc.txt ./
RUN python -m pip install --no-cache-dir -r requirements-doc.txt; exit 0

COPY data ./data
COPY src ./src

CMD ["python", "./src/main.py"]