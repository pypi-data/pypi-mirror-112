# htmlmaker

## Installation

pip3 install htmlmaker

## Usage

from htmlmaker import htmlmaker as hm

```python
fp = open('pure-min.css', 'r', encoding='utf-8')
css = fp.read()
test_table1 = {"title":"my_good_table1", "headers": ["x","y","z"], "body": [{"x": "Title x", "y": "Title y", "z": "Title z"}, {"x": 1, "y": make_anchor("https://www.google.com", "google", True), "z": 3},{"x": 2, "y": 3, "z": 4}]}
test_table2 = {"title":"my_good_table2", "headers": ["x","y","z"], "body": [{"x": "Title x", "y": "Title y", "z": "Title z"}, {"x": 1, "y": make_anchor("https://www.google.com", "google", True), "z": 3},{"x": 2, "y": 3, "z": 4}]}

data = {"tables": [test_table1, test_table2]}
hm.make_output_html('test.html', data, css)
```

## Functions

### make_anchor()

Params: url, content, _blank

### def make_output_html()

Params: output_path, data, css