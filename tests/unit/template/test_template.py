from apex_fastapi.template import setup_template


def test_template():
    templates = setup_template()
    assert templates
