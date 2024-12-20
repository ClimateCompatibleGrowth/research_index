from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestOutput:

    def test_output_list(self):
        response = client.get("/api/outputs")
        assert response.status_code == 200

    def test_output_error_on_not_exist(self):
        response = client.get("/api/outputs/blabla")
        assert response.status_code == 404


class TestAuthor:

    def test_author_list(self):
        response = client.get("/api/authors")
        assert response.status_code == 200

    def test_author_error_on_not_exist(self):
        response = client.get("/api/authors/blabla")
        assert response.status_code == 404


class TestCountry:

    def test_country_list(self):
        response = client.get("/api/countries")
        assert response.status_code == 200

    def test_country_error_on_not_exist(self):
        response = client.get("/api/countries/blabla")
        assert response.status_code == 404


class TestWorkstream:

    def test_workstream_list(self):
        response = client.get("/api/workstreams")
        assert response.status_code == 200

    def test_workstream_error_on_not_exist(self):
        response = client.get("/api/workstreams/blabla")
        assert response.status_code == 404
