from setuptools import setup, find_packages

setup(
    name='canvasTodoist',
    version='0.0.3',
    description='A command line application to transfer canvas assignments to todoist',
    url='https://github.com/lukew3/canvasTodoist',
    author='Luke Weiler',
    author_email='lukew25073@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['todoist-python', 'requests'],
    entry_points={
        'console_scripts': ['canvasTodoist=src.main:main',
                            'canvastodoist=src.main:main'],
    },
)
