raise Exception("""

    kedro-alpiq is a commercial package distributed by Alpiq.
    You have installed a non-functional stub version of the package
    from pypi.org instead of from a private Alpiq repo.
    If you are a [alpiq employee], please ensure you've
    installed kedro-alpiq with the `--extra-index-url` argument,
    either in your requirements.txt file or in the command line,
    so that the package is installed from a private,
    commercial package repository instead of from pypi.org.

""")
