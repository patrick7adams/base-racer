import pytest
import base_racer.main as main

@pytest.mark.parametrize(
    "A,out,baseA,baseB",
    [('1010', '10', 2, 10),
     ('1010', 'a', 2, 16),
    ('111111', '63', 2, 10),
    ('111111', '3f', 2, 16),
    ('10', '1010', 10, 2),
    ('10', 'a', 10, 16),
    ('63', '111111', 10, 2),
    ('63', '3f', 10, 16),
    ('a', '1010', 16, 2),
    ('a', '10', 16, 10),
    ('3f', '111111', 16, 2),
    ('3f', '63', 16, 10)]
)
def test_base_convert(A, out, baseA, baseB):
    # Arrange
    # Act
    result = main.base_convert(A, baseA, baseB)
    # Assert
    assert out == result