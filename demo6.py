from bs4 import BeautifulSoup



s = """
<a> <b>bb<c>cc</c></b> </a>
"""

# b = BeautifulSoup(s, features="lxml")

# b = BeautifulSoup(s, features="xml")

# b = BeautifulSoup(s, features="html.parser")

b = BeautifulSoup(s, features="html5lib")
print(b)

