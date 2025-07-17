# music_maniac_docker
Dockerized version of [Music Maniac Discord Bot](https://github.com/MasterReach1/discord-bots)

# Building

```
git clone https://github.com/nickipp/music_maniac_docker.git
cd music_maniac_docker
docker build -t tagname .
```

# Running

```
docker run -d --restart unless-stopped -e discord_token=token_here --name music_maniac nickipp/music_maniac:latest
```
