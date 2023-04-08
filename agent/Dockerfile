FROM python

WORKDIR /agent

COPY ./agent/requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "./agent/trapAgent.py"]