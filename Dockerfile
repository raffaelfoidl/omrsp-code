# A version with a newer micro version (e. g. 3.7.11) could also be used as micro versions
# generally only consist of bugfixes and do not introduce incompatibilities. As of writing
# this experiment, 3.7.10 is the most recent Python 3.7 version.
FROM python:3.7.10-slim

WORKDIR /home

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY data ./data
COPY src ./src

CMD ["python", "./src/main.py"]