from .conftest import client


def test_entity_404():
    res = client.get("/entities/banana")
    assert res.status_code == 404, res


def test_entity_fetch():
    res = client.get("/entities/Q7747")
    assert res.status_code == 200, res
    data = res.json()
    assert data["id"] == "Q7747"
    assert data["schema"] == "Person"
    assert "wd_curated" in data["datasets"]

    props = data["properties"]
    assert isinstance(props["birthDate"][0], str), props["birthDate"]

    assert "familyPerson" in props
    fam = props["familyPerson"][0]
    assert isinstance(fam, dict), fam
    assert fam["schema"] == "Family", fam

    for fam in props["familyPerson"]:
        famprops = fam["properties"]
        assert len(famprops["relative"]) > 0, famprops
        for rel in famprops["relative"]:
            if isinstance(rel, dict):
                assert rel["id"] != data["id"], rel
            else:
                assert rel != data["id"], rel
        for rel in famprops.get("relative", []):
            if isinstance(rel, dict):
                assert rel["id"] != data["id"], rel
            else:
                assert rel != data["id"], rel
