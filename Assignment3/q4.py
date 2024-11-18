from bs4 import BeautifulSoup
import re

html = """
<html>
<head>
<title>My first web page</title>
</head>
<body>
<h1>My first web page</h1>
<h2>What this is tutorial</h2>
<p>A simple page put together using HTML. <em>I said a simple page.</em>.</p>
<ul>
<li>To learn HTML</li>
<li>
To show off
<ol>
<li>To my boss</li>
<li>To my friends</li>
<li>To my cat</li>
<li>To the little talking duck in my brain</li>
</ol>
</li>
<li>Because I have fallen in love with my computer and want to give her some HTML loving.</li>
</ul>
<h3>Where to find the tutorial</h3>
<p><a href="http://www.aaa.com"><img src=http://www.aaa.com/badge1.gif></a></p>
<h4>Some random table</h4>
<table>
<tr class="tutorial1">
<td>Row 1, cell 1</td>
<td>Row 1, cell 2<img src=http://www.bbb.com/badge2.gif></td>
<td>Row 1, cell 3</td>
</tr>
<tr class="tutorial2">
<td>Row 2, cell 1</td>
<td>Row 2, cell 2</td>
<td>Row 2, cell 3<img src=http://www.ccc.com/badge3.gif></td>
</tr>
</table>
</body>
</html>
"""

# a. Extract the title
title_text = BeautifulSoup(html, "html.parser").title.string
print("a.",title_text)

# b. The text of the second list item element <li> below "To show off".
soup = BeautifulSoup(html, "html.parser")
second_li_text = soup.select_one("ol > li:nth-of-type(2)").text.strip()
print("b.", second_li_text)

# c. All <td> tags in the first row <tr> of the table.
first_row_tds = soup.select("tr.tutorial1 > td")
first_row_tds_text = [td.text.strip() for td in first_row_tds]
print("c.", first_row_tds_text)

# d. All <h2> headings text that includes the word "tutorial".
h2_tutorial = soup.find_all("h2", string=re.compile(r"tutorial", re.IGNORECASE))
h2_tutorial_text = [h2.text.strip() for h2 in h2_tutorial]
print("d.", h2_tutorial_text)

# e. All text that includes the "HTML" word.
html_texts = soup.find_all(string=re.compile(r"HTML", re.IGNORECASE))
html_texts_cleaned = [text.strip() for text in html_texts]
print("e.", html_texts_cleaned)

# f. All text in the second row <tr> of the table.
second_row_tds = soup.select("tr.tutorial2 > td")
second_row_tds_text = [td.text.strip() for td in second_row_tds]
print("f.", second_row_tds_text)

# g. All <img> tags from the table.
table_imgs = soup.select("table img")
table_img_tags = [str(img) for img in table_imgs]
print("g.", table_img_tags)