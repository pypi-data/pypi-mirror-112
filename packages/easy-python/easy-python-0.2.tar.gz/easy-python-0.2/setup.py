from setuptools import setup

readme = open("./README.md", "r")


setup(
    name='easy-python',
    packages=['easy_python'],  # this must be the same as the name above
    version='0.2',
    description='Easy python is an a simple library to learn python in spanish more happy :D',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='PinaYT',
    author_email='pinacomandos@gmail.com',
    # use the URL to the github repo
    url='https://github.com/PinaYTTT/easy_python',
    download_url='https://github.com/PinaYTTT/easy_python',
    keywords=['easy-python', 'learn-easy', 'python3'],
    classifiers=[ ],
    license='MIT',
    include_package_data=True
)