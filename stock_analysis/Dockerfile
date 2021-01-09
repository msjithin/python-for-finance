FROM python:3.9

RUN pip install virtualenv
ENV VIRTUAL_ENV=/venv
RUN virtualenv venv -p python
ENV PATH="VIRTUAL_ENV/bin:$PATH"

WORKDIR .
ADD /assets /data stock_analysis_main.py stock_analysis.py

# Install dependencies
RUN pip install -r requirements.txt
