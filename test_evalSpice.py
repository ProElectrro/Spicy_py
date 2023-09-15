import pytest
import ast
from evalSpice import evalSpice

# Things to be tested
# - Invalid filename: correct message with FileNotFoundError
# - Invalid circuit elements: TypeError with message "Unknown element type"

def test_invalid_file():
    with pytest.raises(FileNotFoundError) as exc_info:
        evalSpice("")
    assert str(exc_info.value) == 'Please give the name of a valid SPICE file as input'

def test_invalid_element():
    with pytest.raises(TypeError) as exc_info:
        evalSpice("test_invalid_element.ckt")
    assert str(exc_info.value) == 'Please give the name of a valid SPICE file as input'


testparams = [
    ("test_1.ckt", "test_1.exp"),
    ("test_2.ckt", "test_2.exp")
   ]

def checkdiff(Vout, Iout, expFile):
    """expected outputs are in `expFile`.  Read and compare."""
    with open(expFile) as f:
        data = f.read()
    (Vexp, Iexp) = ast.literal_eval(data)
    s = 0
    for i in Vexp.keys():
        # print(f"Vexp[{i}] = {Vexp[i]}")
        s += abs(Vexp[i] - Vout[i])
    for i in Iexp.keys():
        for j in Iexp[i].keys():
            # print(f"Iexp[{i}][{j}] = {Iexp[i][j]}")
           s += abs(Iexp[i][j] - Iout[i][j])
    return s

@pytest.mark.parametrize("inFile, expFile", testparams)
def test_spice(inFile, expFile):
    """Test with various input combinations."""
    (Vout, Iout) = evalSpice(inFile)
    assert checkdiff(Vout, Iout, expFile) <= 0.001
