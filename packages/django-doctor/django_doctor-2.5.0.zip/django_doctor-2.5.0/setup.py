from setuptools import find_packages, setup, Extension

from Cython.Build import cythonize


extensions = [
    Extension("django_doctor.staticanalysis.checkers.admin", ["compiled/checkers/admin.c"]),
    Extension("django_doctor.staticanalysis.checkers.migrations", ["compiled/checkers/migrations.c"]),
    Extension("django_doctor.staticanalysis.checkers.model_fields", ["compiled/checkers/model_fields.c"]),
    Extension("django_doctor.staticanalysis.checkers.model_methods", ["compiled/checkers/model_methods.c"]),
    Extension("django_doctor.staticanalysis.checkers.querysets", ["compiled/checkers/querysets.c"]),
    Extension("django_doctor.staticanalysis.checkers.settings", ["compiled/checkers/settings.c"]),
    Extension("django_doctor.staticanalysis.checkers.templates", ["compiled/checkers/templates.c"]),
    Extension("django_doctor.staticanalysis.checkers.urls", ["compiled/checkers/urls.c"]),

    Extension("django_doctor.staticanalysis.checker", ["compiled/checker.c"]),
    Extension("django_doctor.staticanalysis.dependencies", ["compiled/dependencies.c"]),
    Extension("django_doctor.staticanalysis.diff", ["compiled/diff.c"]),
    Extension("django_doctor.staticanalysis.helpers", ["compiled/helpers.c"]),
    Extension("django_doctor.staticanalysis.meta", ["compiled/meta.c"]),
    Extension("django_doctor.staticanalysis.shims", ["compiled/shims.c"]),
    Extension("django_doctor.staticanalysis.suggest", ["compiled/suggest.c"]),
    Extension("django_doctor.staticanalysis.transformer", ["compiled/transformer.c"]),
]

setup(
    name="django_doctor",
    version="2.5.0",
    license="Proprietary. Please purchase a license for commercial use.",
    author="Richard Tier",
    author_email="help@django.doctor",
    url="https://django.doctor",
    description="Find and fix Django mishaps.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    ext_modules=cythonize(extensions),
    entry_points={
        'console_scripts': [
            'django_doctor = django_doctor.staticanalysis.commands.command:main',
        ],
    },
    packages=(
        find_packages(
            include=[
                'django_doctor.wizard',
                'django_doctor.staticanalysis.library_default_settings',
                'django_doctor.staticanalysis.commands'
            ]
        )
    ),
    py_modules=[
        "django_doctor.staticanalysis",  # sdist needs this to include the __init__.py file
        "django_doctor.staticanalysis.constants",
        "django_doctor.staticanalysis.message_templates",
        "django_doctor.staticanalysis.render",
    ],
    include_package_data=True,
    install_requires=[
        "asttokens>=2.0.4,<3.0.0",
        "dparse>=0.5.1,<1.0.0",
        "black>=20.8b0",
        "pylint>=2.5.0,<3.0.0",  # sub requirement astroid.Arguments.arguments needs astroid>=2.4.0
        "rich",
    ],
    extras_require={
        "test": [
            "pytest==5.3.5",
            "pytest-cov",
            "pytest-sugar",
            "pytest-django",
            "django-environ==0.4.5",
            "xeger>=0.3.5,<1.0.0",
            "freezegun>=1.1.0,<2.0.0",
            "WebTest>=2.0.35,<3.0.0",
            "coverage>=5.5.0,<6.0.0",
            "tox",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
