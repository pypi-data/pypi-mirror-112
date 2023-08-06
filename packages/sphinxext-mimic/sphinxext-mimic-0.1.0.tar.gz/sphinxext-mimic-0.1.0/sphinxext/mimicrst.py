def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_directive("mimicrst", mimicrst)
