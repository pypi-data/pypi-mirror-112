import setuptools

setuptools.setup(
    name="google-apis-python-cloudcity",
    version="0.0.2",
    packages=setuptools.find_packages(exclude=("examples","old.*","old")),
    install_requires=[
        "google-api-python-client",
        "wget",
        "google-auth-oauthlib"
    ]
)