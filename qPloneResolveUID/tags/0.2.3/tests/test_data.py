orig_text = """<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Test page for save html rendering including ruid_to_url transformation</title>
<meta name="date" content="2006-08-11" />
</head>
<body>
<h1>Test page</h1>
<table>
<tr>
<th>Test1</th>
<td>test2</td>
</tr>
</table>
<p>This is a text used as a blind text.</p>
<ul>
<li>A sample list item1</li>
<li>A sample list item2</li>
</ul>
<p>This is again a blind text with a<br>line break.</p>
<div>
Can we <q>quote</q> or write something we <del>didn't</del> mean to write? Or how is <ins>this</ins> instead?
</div>
<hr>
<div>
<a href="resolveuid/%s"><img src="resolveuid/%s"/><img src="resolveuid/%s"/></a> is just great.
</div>
</body>
</html>"""
result = """<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Test page for save html rendering including ruid_to_url transformation</title>
<meta name="date" content="2006-08-11" />
</head>
<body>
<h1>Test page</h1>
<table>
<tr>
<th>Test1</th>
<td>test2</td>
</tr>
</table>
<p>This is a text used as a blind text.</p>
<ul>
<li>A sample list item1</li>
<li>A sample list item2</li>
</ul>
<p>This is again a blind text with a<br>line break.</p>
<div>
Can we <q>quote</q> or write something we <del>didn't</del> mean to write? Or how is <ins>this</ins> instead?
</div>
<hr>
<div>
<a href="test1"><img src="test1/test2"/><img src="test1/test2/test3"/></a> is just great.
</div>
</body>
</html>"""