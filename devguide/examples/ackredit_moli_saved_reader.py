"""Read the saved synthetic #76 example in a fresh process without new use.

Usage: python -I ackredit_moli_saved_reader.py saved-example.json
The saved outer wrapper belongs only to the companion example.
"""

import importlib
import importlib.abc
import json
import socket
import sys
from pathlib import Path


class ExcludeProducerEngines(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in {"sabueso", "pint", "unyt", "pyunitwizard"}:
            raise AssertionError("saved reader loaded an original engine")


def prohibit_network(*args, **kwargs):
    raise AssertionError("saved reader attempted network access")


def main():
    sys.meta_path.insert(0, ExcludeProducerEngines())
    socket.create_connection = prohibit_network
    socket.socket.connect = prohibit_network
    ackredit = importlib.import_module("ackredit")
    original = json.loads(Path(sys.argv[1]).read_text())
    with ackredit.session("fresh-reader"):
        for result in original["results"]:
            restored = ackredit.Attribution.from_dict(result["attribution"])
            assert restored.to_dict() == result["attribution"]
            assert restored.to_dict()["context"]["producer"]["version"] == "1"
            assert all(
                item["version"] in {"1", "revision-1"}
                for item in restored.to_dict()["items"]
            )
        empty = ackredit.get_attribution().to_dict()
        assert empty["items"] == [] and empty["uses"] == []
    print(
        json.dumps(
            {
                "state": "passed",
                "results": len(original["results"]),
                "new_credits": 0,
                "original_records": "unchanged",
                "producer_engines": "prohibited",
                "network": "prohibited",
            }
        )
    )


if __name__ == "__main__":
    main()
