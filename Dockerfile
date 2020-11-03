FROM python:3.7-slim-buster
LABEL maintainer="trasformer: @kekmarakek"

WORKDIR /app

COPY . .

CMD /bin/bash

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r Requirements.txt

ENTRYPOINT ["python", "./bot.py"]
EXPOSE 80