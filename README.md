# Correct Vietnamese Sentence tool
## Description
* Adding accents vietnamese sentence tool

## Intsallation
<code> pip install vicorrect</code>

## Examples:
```python
from vicorrect.model import CorrectVietnameseSentence

dataset = """
trời buồn trời đổ cơn mưa
chim khôn chim đậu cành đa"""

corrector = CorrectVietnameseSentence(verbose=False)
corrector.fit(dataset.splitlines())

testcase = [
    "troi buon",
    "com chim dau",
    "chim dau canh da troi do mua"
]

print(corrector.predict(testcase))
```
## Author
**Hanh. Le Van**
