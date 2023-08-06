from distutils.core import setup

setup(
    name='napit',
    packages=['napit'],
    version='1.0',
    license='MIT',
    description='A naver api translate client',
    author='dolphin2410',
    author_email='dolphin2410@outlook.kr',
    url='https://github.com/dolphin2410/napit',
    download_url='https://github.com/dolphin2410/napit/archive/refs/tags/1.0.tar.gz',
    keywords=['rest', 'api', 'naver'],
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)