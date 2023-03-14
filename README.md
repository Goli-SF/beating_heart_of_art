# Beating Heart of Art

## Description

This project involves the analysis of artworks from the API of the Metropolitan Museum of Art using CNNs and mapping the results on the world map to visualize the circulation of artistic styles across continents and centuries.

## Build docker image

```bash
docker build -t beating_heart_of_art:dev .
```

## Run docker container

```bash
docker run -it --rm -p 8000:8000 beating_heart_of_art:dev
```

## Bash into docker container

```bash
docker run -it beating_heart_of_art:dev bash
```
