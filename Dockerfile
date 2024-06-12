FROM python:3.8

WORKDIR /app
RUN pip install 'transformers[torch]'

COPY requirements.txt ./
RUN pip install -r requirements.txt

RUN mkdir results data
COPY data/message-db.json data/users.json ./data/
COPY results/ ./results/

COPY chat.py constants.py discord_bot.py llm.py messages.py util.py ./

CMD python3 discord_bot.py