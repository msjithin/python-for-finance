FROM python:3.9

# RUN pip install virtualenv
# ENV VIRTUAL_ENV=/venv
# RUN virtualenv venv -p python
# ENV PATH="VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt ./requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

EXPOSE 8080

WORKDIR /stock_analysis

COPY . /stock_analysis

CMD streamlit run --server.port 8080 --server.enablrCORS false stock_analysis_main.py 



