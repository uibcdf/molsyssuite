"""Synthetic application example for uibcdf/molsyssuite#76 / uibcdf/moli#36.

Run with installed Ackredit >=0.9.0. The outer dictionaries below belong only
to this example; they define no shared result, acquisition or project schema.
No source is contacted and no scientific result or permission is inferred.
"""

import json
from importlib.metadata import version

import ackredit


def main():
    producer = {"name": "synthetic-suite-application", "version": "1"}
    results = []
    operations = []
    resource = "example:synthetic-resource:revision-1"
    software = "example:synthetic-application:1"

    with ackredit.session("synthetic-two-result-workflow"):
        ackredit.register_item(
            id=resource,
            type="dataset",
            title="Synthetic resource; no real source or bibliography claimed",
            version="revision-1",
        )
        ackredit.register_item(
            id=software,
            type="software",
            title="Synthetic suite application",
            version="1",
        )
        for name, fixture in (("result-1", ["synthetic-row"]), ("result-2", [])):
            context = {"result": name, "producer": producer, "synthetic": True}
            with (
                ackredit.capture(name, context=context) as observed,
                ackredit.scope(name),
            ):
                # A real in-memory operation, deliberately replacing network
                # acquisition. Reading [] completes with an empty answer.
                value = list(fixture)
                operation = {
                    "id": name + ":fixture-read",
                    "result": name,
                    "route": "in-memory-fixture",
                    "outcome": "acquired" if value else "evaluated-empty",
                    "resource_revision": "revision-1",
                    "network_attempts": 0,
                }
                operations.append(operation)
                ackredit.track_item(
                    resource,
                    roles=["observed_resource_use"],
                    context={**context, "operation": operation["id"]},
                )
                ackredit.track_item(
                    software,
                    roles=["executed_software"],
                    context=context,
                )
            results.append(
                {
                    "id": name,
                    "producer": producer,
                    "value": value,
                    "calculation_status": "completed",
                    "attribution_status": "captured-observed-uses",
                    "attribution": observed.attribution.to_dict(),
                    "source_support": [],
                    "source_terms": {"status": "unknown"},
                }
            )

        # The application owns this failed attempt and its incomplete status.
        # A provider capture cannot turn failure into completed resource use.
        try:
            raise LookupError("deliberately unavailable synthetic extra resource")
        except LookupError as error:
            operations.append(
                {
                    "id": "result-2:failed-extra",
                    "result": "result-2",
                    "outcome": "failed",
                    "error": str(error),
                    "network_attempts": 0,
                }
            )
            results[1]["acquisition_status"] = "partial"

        workflow = ackredit.get_attribution().to_dict()
        # Saving and reading retain original records without creating new uses.
        saved = json.dumps(results)
        restored = json.loads(saved)
        for result in restored:
            assert (
                ackredit.Attribution.from_dict(result["attribution"]).to_dict()
                == result["attribution"]
            )
        assert ackredit.get_attribution().to_dict() == workflow

    # A separate reader session sees no credit from importing saved records.
    with ackredit.session("saved-reader"):
        for result in restored:
            ackredit.Attribution.from_dict(result["attribution"]).to_json()
        reader = ackredit.get_attribution().to_dict()
        assert reader["items"] == [] and reader["uses"] == []

    for result in restored:
        assert {item["id"] for item in result["attribution"]["items"]} == {
            resource,
            software,
        }
        assert result["attribution"]["context"]["producer"] == producer
    assert len(workflow["items"]) == 2
    assert len(workflow["uses"]) == 4
    assert len(results[1]["attribution"]["uses"]) == 2
    print(
        json.dumps(
            {
                "example_only": True,
                "ackredit_version": version("ackredit"),
                "results": restored,
                "host_operations": operations,
                "workflow_attribution": workflow,
                "saved_reader": reader,
                "project_interpretation": {"status": "pending-owner-decision"},
                "authorization": {"status": "undecided"},
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
