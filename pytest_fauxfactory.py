# -*- coding: utf-8 -*-
def pytest_namespace():
    """Inject the fauxfactory module into the pytest namespace using ``faux`` name."""
    import fauxfactory
    return {'faux': fauxfactory}
