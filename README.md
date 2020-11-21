# text_trasformer_bot
Changes the direction of the text

Install requirements from file
```bash
sudo python3 -m pip install -r Requirements.txt
```

For tests you can start the bot from CLI:
```bash
python3 bot.py
```

#Docker
build
```bash
docker build -t text_trasformer_bot .
```
run
```bash
docker run -d -p port:port text_trasformer_bot
```