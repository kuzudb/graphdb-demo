# Unity Catalog Community Meetup

Code for the demo presented at the Unity Catalog Community Meetup on 15 May 2025. The demo shows
how to use query and run a NetworkX graph workflow on data that comes from Unity Catalog.

## Prerequisites

- Install the dependencies listed in the `requirements.txt` file.
- Have a locally running Unity Catalog server, see the [quick start guide](https://docs.unitycatalog.io/quickstart/) for details.
Once the server is successfully running, the example data files will be present at this location on your local filesystem.

```bash
# Use uv to install the dependencies
uv pip install -r requirements.txt
```

```bash
# Run the script
uv run workflow.py
```

You can also interactively run the code line by line via `ipykernel` in your local IDE like VSCode or Cursor.


