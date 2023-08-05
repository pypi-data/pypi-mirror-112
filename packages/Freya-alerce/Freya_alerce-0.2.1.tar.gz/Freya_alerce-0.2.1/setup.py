from setuptools import setup,find_packages

setup(
      name='Freya_alerce',
      version='0.2.1',
      author='Eric "Jonimott" Fernández',
      author_email='',
      description='Freya is a Python framework that quick development queries in astronomical catalogs and use local or creating easy new API called FreyaAPI',
      url='https://github.com/fernandezeric/Freya',
      license='',
      packages=find_packages(),
      #include_package_data=True,
      package_data = {
            'Freya_alerce.core': ['*.txt'],
            'Freya_alerce.files.file_templates': ['*.zip']
      },
      entry_points = {
            'console_scripts': ['freya-admin=Freya_alerce.freya:Main.main'],
      },
      zip_safe=False,
      classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Natural Language :: English"
      ],
      test_suite="tests",
      python_requires='>=3.9',
      install_requires=[i.strip() for i in open("requirements.txt").readlines()]
)