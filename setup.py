import setuptools

setuptools.setup(
    pbr=True,
    package_data={
        "sparrow": [
            '*.yaml', '*.yml',
            'api/static/*'
        ],
    },
)
