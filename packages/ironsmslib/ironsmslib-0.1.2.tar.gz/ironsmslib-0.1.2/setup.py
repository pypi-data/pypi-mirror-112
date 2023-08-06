from setuptools import setup

setup(
    name='ironsmslib',
    version='0.1.2',
    packages=['ironsms', 'ironsms.api', 'ironsms.types', 'ironsms.exceptions'],
    url='https://github.com/viuipan/ironsmslib',
    license='MIT',
    author='viuipan',
    author_email='viuipan@gmail.com',
    description='Library for API iron-sms.com',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=[
        'httpx',
        'pydantic'
    ]
)
