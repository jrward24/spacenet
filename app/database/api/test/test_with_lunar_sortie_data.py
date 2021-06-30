import pprint
from typing import Union

import pytest
from fastapi.testclient import TestClient

from app.database.api.database import get_db
from app.database.api.main import app
from ..schemas.constants import CREATE_SCHEMAS
from app.database.api.test.utilities import get_test_db
from spacenet.schemas import EdgeType, ElementKind, NodeType, ResourceType
from spacenet.test.utilities import (
    lunar_sortie_elements,
    lunar_sortie_edges,
    lunar_sortie_nodes,
    lunar_sortie_resources,
    KIND_TO_SCHEMA,
)

pytestmark = [pytest.mark.unit, pytest.mark.database, pytest.mark.lunar_sortie]

app.dependency_overrides[get_db] = get_test_db

client = TestClient(app)

TYPE_TO_PREFIX = {
    ElementKind: "element",
    EdgeType: "edge",
    NodeType: "node",
    ResourceType: "resource",
}


def object_to_prefix(obj: dict) -> str:
    for schema in CREATE_SCHEMAS:
        try:
            obj = schema.parse_obj(obj)
        except ValueError:
            pass
        else:
            pprint.pprint(obj)
            return TYPE_TO_PREFIX[type(obj.type)]


@pytest.mark.parametrize(
    "domain_objects",
    (
            pytest.param(
                pytest.lazy_fixture("lunar_sortie_" + obj_type + "s"),
                marks=getattr(pytest.mark, obj_type),
            )
            for obj_type in ["element", "edge", "node", "resource"]
    ),
)
def test_routers_with_lunar_sortie_data(domain_objects):
    for obj in domain_objects:
        prefix = object_to_prefix(obj)
        post_response = client.post(f"/{prefix}/", json=obj)
        assert 201 == post_response.status_code
        result = post_response.json()
        id_ = result.get("id")
        with_id = dict(obj, id=id_)
        assert with_id == result
        get_response = client.get(f"/{prefix}/{id_}")
        assert 200 == get_response.status_code
        assert with_id == get_response.json()
        delete_response = client.delete(f"/{prefix}/{id_}")
        assert 200 == delete_response.status_code
        assert with_id == delete_response.json()
        assert 404 == client.get(f"/{prefix}/{id_}").status_code
