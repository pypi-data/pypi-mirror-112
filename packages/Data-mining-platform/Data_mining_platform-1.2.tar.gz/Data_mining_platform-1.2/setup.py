from distutils.core import setup

# from setuptools import setup, find_packages


setup(
    name='Data_mining_platform',
    version='1.2',
    packages=['codes','Mytest','files'],
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst','*.pdf'],
    },

    install_requires=[
        'xgboost==1.3.3',
        'tsfresh==0.18.0',
        'category_encoders==2.2.2',
        'seaborn==0.10.1',
        'dcor==0.5.3',
        'numpy==1.18.5',
        'statsmodels==0.11.1',
        'matplotlib==3.2.2',
        'pandas==1.1.4',
        'minepy==1.2.5',
        'lightgbm==3.1.1',
        'scipy==1.5.2',
        'scikit_learn==0.23.1'],
    zip_safe=False

)  ##zklhdzhbg





