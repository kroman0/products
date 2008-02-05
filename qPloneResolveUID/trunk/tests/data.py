orig_text = """
<html>
  <body>
    <h1>Test page</h1>
    <div>
      <a href="resolveuid/%s"/>
      <img src="resolveuid/%s"/>
      <img src="resolveuid/%s"/>
      <a href="resolveuid/%s"/>
      <a href="resolveuid/thisisuidtodeletedobject">
    </div>
  </body>
</html>"""
result = """
<html>
  <body>
    <h1>Test page</h1>
    <div>
      <a href="/test1"/>
      <img src="/test1/test2"/>
      <img src="/test1/test2/image_mini"/>
      <a href="/folder2/docintoplevelfolder"/>
      <a href="resolveuid/thisisuidtodeletedobject">
    </div>
  </body>
</html>"""
