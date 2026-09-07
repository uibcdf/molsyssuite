def test_package_imports():
    import __PACKAGE_NAME__

    assert __PACKAGE_NAME__.__doc__
