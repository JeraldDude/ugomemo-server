class NintendoConnectionTest:
    """
    Authentic Nintendo Connection Test index page.
    This is the REAL content Nintendo served at GET /.
    The DSi only checks for HTTP 200 OK, so this HTML is ignored by the console
    but is 100% accurate to the original server.
    """

    INDEX_PAGE = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
  <title>HTML Page</title>
</head>
<body bgcolor="#FFFFFF">
This is test.html page
</body>
</html>"""

    def handle_root(self) -> str:
        """
        Return the authentic Nintendo index page.
        """
        return self.INDEX_PAGE

    def handle_any(self, path: str) -> str:
        """
        Nintendo returned the same HTML for ANY path.
        """
        return self.INDEX_PAGE
