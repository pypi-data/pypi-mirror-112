from setuptools import setup, find_packages

setup(
    name='MOTUS',
    version='0.9',
    description='Paquetería para el Análisis Conductual de Patrones de Desplazamiento',
    author='Escamilla, Toledo, Tamayo, Avendaño, León, Eslava, Hernández',
    author_email='escamilla.een@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
    ],
)