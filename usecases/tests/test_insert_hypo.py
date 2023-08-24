
from unittest.mock import Mock
import pytest
from mrplatobackend.mrplatoweb.mrplatoweb.main import ProofWindow,InputAdditionalForm

from usecases import InsertHypothesis

pytestmark = pytest.mark.unit


class TestInsertHypo:

    def test_insert_valid(self):
        data = ['∼', ['p', '∧', 'q']]
        insert = InsertHypothesis(proofwindow=ProofWindow(), inputadditionalform=InputAdditionalForm())
        result = insert.insert(data)

        assert result["success"] == True


    def test_insert_invalid(self):
        data = "['∼', ['p', '∧', 'q']]"
        insert = InsertHypothesis(proofwindow=ProofWindow, inputadditionalform=InputAdditionalForm)
        result = insert.insert(data)

        assert result["success"] == False