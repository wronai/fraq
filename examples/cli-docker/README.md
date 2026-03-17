# CLI + fraq w Docker

Uruchamiaj fraq CLI w kontenerze Docker.

## Szybki start

```bash
cd examples/cli-docker

# Budowa obrazu
docker-compose build

# Uruchomienie z domyślną komendą (help)
docker-compose run --rm fraq-cli

# Wyszukaj pliki w zamontowanym folderze
docker-compose run --rm fraq-cli fraq files search --ext pdf --limit 10 /data

# Eksploruj fraktal
docker-compose run --rm fraq-cli fraq explore --depth 5 --format json
```

## Użycie bez docker-compose

```bash
# Zbuduj obraz
docker build -t fraq-cli .

# Uruchom z volume
docker run --rm -v $(pwd)/data:/data fraq-cli \
    fraq files search --ext py --limit 5 /data
```

## Przykłady

```bash
# Wyszukaj PDFy w /home (zamontowany z hosta)
docker-compose run --rm fraq-cli \
    fraq files search --ext pdf --limit 10 /data

# Natural language
docker-compose run --rm fraq-cli \
    fraq nl "show 10 temperature readings"

# Statystyki pliku
docker-compose run --rm fraq-cli \
    fraq files stat /data/README.md
```

## Konfiguracja

Edytuj `docker-compose.yml` aby zmienić zamontowane ścieżki:
```yaml
volumes:
  - /home:/data:ro  # zamontuj /home z hosta
```
