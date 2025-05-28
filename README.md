<h1 align="center">Invader Spotter News</h1>
<h3 align="center">Get invader news from a telegram channel bot</h3>

---

<p align="center">
<img alt="Logo Banner" src="assets/banner.jpg?sanitize=true"/>
</p>

<br/>
<br/>

<p align="center">
<a href="https://github.com/GestaltCaius/telegram-news-chat-bot/releases">
<img alt="Current Release" src="https://img.shields.io/github/release/GestaltCaius/telegram-news-chat-bot.svg"/>
</a>
<a href="https://hub.docker.com/r/GestaltCaius/telegram-news-chat-bot">
<img alt="Docker Pull Count" src="https://img.shields.io/docker/pulls/GestaltCaius/telegram-news-chat-bot.svg"/>
</a>
</p>

---

Scrapes [Invader Spotter news page](https://www.invader-spotter.art/news.php), and sends data to channels (e.g. Telegram, Twitter, Bluesky, etc.).

The only currently working channel is the telegram one. More coming soon.

# How to build and deploy

```sh
# auth
gcloud auth configure-docker us-docker.pkg.dev

export DOCKER_IMAGE="gcr.io/${GCP_PROJECT_ID}/${GCP_REPO_NAME}:${VERSION}"

# build and push
docker build \
  -t "${DOCKER_IMAGE}" \
  .

docker push "${DOCKER_IMAGE}"

# deploy cloud run job
gcloud run jobs create \
  spotter-bot-service \
  --image "${DOCKER_IMAGE}" \
  --region europe-west1 \
  --set-env-vars TELEGRAM_BOT_TOKEN="${BOT_API_TOKEN}",TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID}"
```