from setuptools import setup

README = 'README.md'

with open(README) as file:
    longDescription = file.read()

setup(
    name='archfinder',
    version='0.0.2',
    description='Arch Linux mirrorlist builder for pacman',
    long_description=longDescription,
    long_description_content_type='text/markdown',
    author='Francisco Braço-Forte',
    author_email='f.s.f.b2001@gmail.com',
    license='GPL-3.0-or-later',
    license_files=[
        'LICENSE'
    ],
    python_requires='>=3.8, <4',
    packages=[
    	'archfinder'
    ],
    package_dir={
    	"": "src"
    },
    install_requires=[
        'urllib3==1.26.5'
    ],
    zip_safe=False,
    entry_points={
        'console_scripts' : [
                'archsfinder=archsfinder.archfinder:main'
        ]
    }  
)
