# Install from GitHub ppa

```
curl -s --compressed "https://eternalconcert.github.io/ppa/KEY.gpg" | sudo apt-key add -
sudo curl -s --compressed -o /etc/apt/sources.list.d/github_ppa.list "https://eternalconcert.github.io/ppa/files.list"

sudo apt update
sudo apt install anvil

```
