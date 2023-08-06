from distutils.core import setup

setup(
    name='simalia',
    packages=['simalia'],
    version='0.0.1',
    license='MIT',
    description='Python web framework',
    author='seyed sadegh shobeiry',
    author_email='ssshobeiry@gmail.com',
    url='https://github.com/simalia/core',
    download_url='https://github.com/simalia/core/archive/refs/heads/main.zip',
    keywords=['simalia', 'python', 'web', 'framework'],
    install_requires=[
        'python-dotenv',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
