<div align="center">
<p align="center">

<img width="275" alt="Kùzu logo" src="https://kuzudb.com/img/kuzu-logo.png">

**An in-process graph database built for query speed and scalability**

[![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/VtX2gw9Rug)
[![Twitter](https://img.shields.io/badge/Twitter-%231DA1F2.svg?style=for-the-badge&logo=Twitter&logoColor=white)](https://twitter.com/kuzudb)
</p>

</div>

# Graph demos and use cases

This repo contains recipes and starter code for various graph use cases in Kùzu. Feel free to clone/fork the repo and modify the code for your own projects!

## Getting Started

In addition to a [command line tool](https://kuzudb.com/docusaurus/getting-started/cli), Kùzu has a number of client libraries available that allow you to interface with the database in your language of choice. Currently, the following languages are supported:

- Python
- Node.js
- C++
- C
- Java
- Rust

You can find the latest list of language clients in the [docs](https://docs.kuzudb.com/client-apis/).

## Setting up Kùzu

Kùzu is an embedded database that runs in-process, so there's no server to set up. Simply install the client library for your language of choice and you're ready to go! A couple of examples are shown below.

### Python

For Python users using local Jupyter notebooks or Python scripts, simply install the `kuzu` package via `pip`.

```bash
# Set up a virtual environment
python -m venv venv
source venv/bin/activate
# Assuming Python 3.8+ is installed
pip install kuzu
```

### JavaScript

For Node.js users, install the `kuzu` package via `npm`.

```bash
# Assuming Node.js 19+ is installed
npm install kuzu
```