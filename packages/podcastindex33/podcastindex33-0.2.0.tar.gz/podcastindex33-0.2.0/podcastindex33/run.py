import typer

import json
from typing import Optional, List

import podcastindex33 as pci


def main(
  method: str,
  api_key: str = typer.Argument(None, envvar="PCI_API_KEY"),
  api_secret: str = typer.Argument(None, envvar="PCI_API_SECRET"),
  args: Optional[List[str]] = [],
):
  api = pci.PodcastIndex(api_key, api_secret)
  result = getattr(api, method)(*args)
  print(json.dumps(result, indent=2))

def run ():
  typer.run(main)

if __name__ == "__main__":
  run()
