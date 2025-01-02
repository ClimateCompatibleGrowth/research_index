from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestOutput:

    def test_output_list(self):
        response = client.get("/outputs")
        print("response=" + str(response.text))
        assert response.status_code == 200

    def test_output_list_limit(self):
        response = client.get("/outputs?limit=1")
        assert response.status_code == 200

    def test_output_list_limit_skip(self):
        response = client.get("/outputs?limit=1&skip=1")
        assert response.status_code == 200

    def test_output_list_limit_skip_result_type(self):
        response = client.get("/outputs?limit=1&skip=1&result_type=publication")
        assert response.status_code == 200

    def test_output_list_limit_skip_result_type_wrong(self):
        response = client.get("/outputs?limit=1&skip=1&result_type=notallowed")
        assert response.status_code == 422

    def test_output_error_id_wrong_format(self):
        response = client.get("/outputs/blabla")
        assert response.status_code == 422

    def test_output_error_not_exist(self):
        response = client.get("/outputs/97c945d6-e172-4e7f-8a3a-02a7a51ae62b")
        assert response.status_code == 404



class TestAuthor:

    def test_author_list(self):
        response = client.get("/authors")
        assert response.status_code == 200

    def test_author_not_exist(self):
        response = client.get("/authors/8119878e-1875-4cdf-a6a8-a9025057ddc6")
        assert response.status_code == 404

    def test_author_list(self):
        response = client.get("/authors")
        assert response.status_code == 200

    def test_author_list_limit(self):
        response = client.get("/authors?limit=1")
        assert response.status_code == 200

    def test_author_list_limit_skip(self):
        response = client.get("/authors?limit=1&skip=20")
        assert response.status_code == 200

    def test_author_list_skip_negative(self):
        response = client.get("/authors?skip=-1")
        assert response.status_code == 422

    def test_author_list_limit_zero(self):
        response = client.get("/authors?limit=0")
        assert response.status_code == 422

    def test_author_error_on_author_id_wrong_format(self):
        response = client.get("/authors/blabla")
        assert response.status_code == 422

    def test_author_error_on_author_id_not_exist(self):
        response = client.get("/authors/97c945d6-e172-4e7f-8a3a-02a7a51ae62b")
        assert response.status_code == 404

    def test_author_workstream(self):
        response = client.get("/authors?workstream=ws7a")
        assert response.status_code == 200

    def test_author_multiple_workstream(self):
        response = client.get("/authors?workstream=ws7a&workstream=ws5a")
        assert response.status_code == 200


class TestCountry:

    def test_country_list(self):
        response = client.get("/countries")
        assert response.status_code == 200

    def test_country_list_skip(self):
        response = client.get("/countries?skip=1")
        assert response.status_code == 200

    def test_country_list_limit(self):
        response = client.get("/countries?limit=1")
        assert response.status_code == 200

    def test_country_list_limit_illegal(self):
        response = client.get("/countries?limit=0")
        assert response.status_code == 422

    def test_country_raise_warning_on_bad_id(self):
        response = client.get("/countries/blabla")
        assert response.status_code == 422

    def test_country_detail_skip(self):
        response = client.get("/countries/KEN?skip=1")
        assert response.status_code == 200

    def test_country_detail_limit(self):
        response = client.get("/countries/KEN?limit=1")
        assert response.status_code == 200

    def test_country_detail_limit_illegal(self):
        response = client.get("/countries/KEN?limit=0")
        assert response.status_code == 422

    def test_country_error_on_not_exist(self):
        """Meets
        """
        response = client.get("/countries/XXX")
        assert response.status_code == 404


class TestWorkstream:

    def test_workstream_list(self):
        response = client.get("/workstreams")
        assert response.status_code == 200

    def test_workstream_error_on_not_exist(self):
        """Meets
        """
        response = client.get("/workstreams/XXX")
        assert response.status_code == 404
