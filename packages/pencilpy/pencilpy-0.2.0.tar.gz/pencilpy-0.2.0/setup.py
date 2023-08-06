from setuptools import setup

setup(
    name='pencilpy',
    version='0.2.0',    
    description='Get pencil sketches from image',
    url='https://github.com/dingus45191/pencil-cartoon',
    author='MOhammed Mubashir Hasan',
    author_email='mubashirhasan716@gmail.com',
    license='BSD 2-clause',
    packages=['pencilpy'],
    install_requires=['opencv-python',
                      'numpy',                     
                      ],

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)