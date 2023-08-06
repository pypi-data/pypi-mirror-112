from distutils.core import setup

setup(
  name = 'cargoproduce',        
  packages = ['cargoproduce'],  
  version = '2.1.4',      
  license='MIT',       
  description = 'QLDB low level drivers',  
  author = 'German Basisty',                 
  author_email = 'german@cargoproduce.com',     
  url = 'https://github.com/CargoProduce/cargo-produce-python-modules',  
  download_url = 'https://github.com/CargoProduce/cargo-produce-python-modules/archive/refs/tags/v_09.tar.gz',
  keywords = ['QLDB', 'Low level driver'],  
  install_requires=[     
          'pyqldb==3.1.0',
          'jsonconversion',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',    
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
