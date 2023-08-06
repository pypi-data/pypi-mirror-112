from distutils.core import setup

setup(
    name='rxjwt',
    packages=['rxjwt', 'rxjwt.migrations'],
    version='1.2',
    license='MIT',
    description='This library provides user authorization functions through '
                'JSON Web Token (JWT) mechanism.',
    author='Mikhail Kormanowsky',
    author_email='kormanowsky@gmail.com',
    url='https://github.com/kormanowsky/rxjwt',
    download_url='https://github.com/kormanowsky/rxjwt/archive/refs/tags/v1.2.tar.gz',
    keywords=['Django', 'django-rest', 'django-auth'],
    install_requires=[
        'Django',
        'djangorestframework',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
