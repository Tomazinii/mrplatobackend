import pytest
from usecases import IntegrationMrplato


pytestmark = pytest.mark.unit


class TestIntegration:
    
    def test_apply(self):
        integration = IntegrationMrplato()
        

        assert 1 == 1