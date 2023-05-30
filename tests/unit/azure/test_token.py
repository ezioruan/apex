from apex_fastapi.azure.token import verify_azure_token


def test_verfy_azure_token():
    access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxM"
    result = verify_azure_token(access_token)
    assert result["message"]
