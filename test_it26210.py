from it26210 import api_status_matcher

def test_api_status_matcher() -> bool:
    status = 402
    assert api_status_matcher(status) == False
    status = 611
    assert api_status_matcher(status) == False
    status = 0
    assert api_status_matcher(status) == True
    status = "any"
    assert api_status_matcher(status) == False