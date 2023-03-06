# Beating Heart of Art

## Description

This project involves the analysis of artworks from the API of the Metropolitan Museum of Art using CNNs and mapping the results on the world map to visualize the circulation of artistic styles across continents and centuries.

## Python package management

The project uses [Poetry](https://python-poetry.org/) for package management. To install Poetry, follow the instructions on the [official website](https://python-poetry.org/docs/#installation).

Each project and library has its own virtual environment. To create a new virtual environment, run the following command in the project or library directory:

```bash
poetry install
```

To initialize a new project, run the following command in the new project directory:

```bash
poetry init
```

To activate the virtual environment, run the following command:

```bash
poetry shell
```

Alternatively, you can run the following command to run a command in the virtual environment:

```bash
poetry run <command>
```

To add a new dependency, run the following command:

```bash
poetry add <package>
```

To add a development dependency, run the following command:

```bash
poetry add --dev <package>
```

To remove a dependency, run the following command:

```bash
poetry remove <package>
```

To update all dependencies, run the following command:

```bash
poetry update
```

To export the list of dependencies to a file, run the following command:

```bash
poetry export -f requirements.txt --output requirements.txt
```

## Code structure
