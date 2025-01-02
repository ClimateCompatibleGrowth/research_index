from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestOutput:
    def test_output_list(self):
        response = client.get("/api/outputs")
        print("response=" + str(response.text))
        assert response.status_code == 200

    def test_output_list_limit(self):
        response = client.get("/api/outputs?limit=1")
        assert response.status_code == 200

    def test_output_list_limit_skip(self):
        response = client.get("/api/outputs?limit=1&skip=1")
        assert response.status_code == 200

    def test_output_list_limit_skip_result_type(self):
        response = client.get("/api/outputs?limit=1&skip=1&result_type=publication")
        assert response.status_code == 200

    def test_output_list_limit_skip_result_type_wrong(self):
        response = client.get("/api/outputs?limit=1&skip=1&result_type=notallowed")
        assert response.status_code == 422

    def test_output_error_id_wrong_format(self):
        response = client.get("/api/outputs/blabla")
        assert response.status_code == 422

    def test_output_error_not_exist(self):
        response = client.get("/api/outputs/97c945d6-e172-4e7f-8a3a-02a7a51ae62b")
        assert response.status_code == 404


class TestAuthor:

    def test_author_list(self):
        response = client.get("/api/authors")
        assert response.status_code == 200

    def test_author_list_limit(self):
        response = client.get("/api/authors?limit=1")
        assert response.status_code == 200

    def test_author_list_limit_skip(self):
        response = client.get("/api/authors?limit=1&skip=20")
        assert response.status_code == 200

    def test_author_list_skip_negative(self):
        response = client.get("/api/authors?skip=-1")
        assert response.status_code == 422

    def test_author_list_limit_zero(self):
        response = client.get("/api/authors?limit=0")
        assert response.status_code == 422

    def test_author_error_on_author_not_exist(self):
        response = client.get("/api/authors/blabla")
        assert response.status_code == 422


class TestCountry:

    def test_country_list(self):
        response = client.get("/api/countries")
        assert response.status_code == 200

    def test_country_raise_warning_on_bad_id(self):
        response = client.get("/api/countries/blabla")
        assert response.status_code == 422

    def test_country_error_on_not_exist(self):
        """Meets
        """
        response = client.get("/api/countries/XXX")
        assert response.status_code == 404