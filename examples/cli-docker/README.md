# CLI + fraq w Docker

Uruchamiaj fraq CLI w kontenerze Docker.

## Szybki start (skrypt)

```bash
cd examples/cli-docker

# Uruchom CLI w Docker
./run.sh fraq files search --ext pdf --limit 10 /data

# Lub przez Python wrapper
python run.py files search --ext py --limit 5 /data

# Uruchom lokalnie (bez Docker)
python run.py --local explore --depth 3
```

## Szybki start (docker-compose)

```bash
cd examples/cli-docker

# Budowa obrazu
docker-compose build

# Uruchomienie z domyślną komendą (help)
docker-compose run --rm fraq-cli

# Wyszukaj pliki w zamontowanym folderze
docker-compose run --rm fraq-cli fraq files search --ext pdf --limit 10 /data
```

## Uruchamialne pliki

| Plik | Opis |
|------|------|
| `run.sh` | Bash wrapper do CLI w Docker |
| `run.py` | Python wrapper: `python run.py [fraq args]` |
| `Dockerfile` | Obraz z fraq CLI |
| `docker-compose.yml` | Konfiguracja z zamontowanymi voluminami |
