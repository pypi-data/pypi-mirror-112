import setuptools
setuptools.setup(
    name='berry_video',
    version='0.0.2',
    scripts=['script/berry'],
    author='Mr Menezes',
    author_email='sr.tama@outlook.com',
    license='@copyright',
    description='Tools of berry video',
    packages=['berry_video'],
    install_requires=[
        'setuptools',
        'google-api-python-client==2.12.0',
        'oauth2client==4.1.3',
        'python_crontab==2.5.1',
    ],
    python_requires='>=3.5'
)