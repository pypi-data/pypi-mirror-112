from setuptools import setup, find_packages

setup(
    name='piotr',
    version='1.0.1',
    description='Piotr is an instrumentation tool for qemu-system-arm able to emulate ARM-based embedded devices.',
    long_description='''Piotr provides an easy way to create, run and share virtual IoT devices. It is suitable for
trainings (especially remote trainings) where embedded device emulation is required. 

Piotr provides a set of useful command-line utilities to manage the emulated devices and interact with them,
and a Python API to allow automation. Thus, it is easy to spawn an emulated device, interact with its system,
remotely debug a specific process and exploit some vulnerabilities for instance.''',
    url='https://github.com/virtualabs/piotr',
    author='virtualabs',
    author_email='virtualabs@gmail.com',
    packages=find_packages('src'),
    package_dir={"":"src"},
    package_data = {
        'piotr':[
            'data/*'
        ]
    },
    classifiers=['Development Status :: 4 - Beta'],
    entry_points = {
        'console_scripts': [
            'piotr=piotr:main',
            'piotr-shell=piotr.shell:guest_shell',
            'piotr-ps=piotr.shell:host_ps',
            'piotr-debug=piotr.shell:debug_process'
        ],
    },
    install_requires = [
        'blessings',
        'psutil',
        'pyyaml'
    ],
    python_requires='>=3.5',
    test_suite='tests'
)
