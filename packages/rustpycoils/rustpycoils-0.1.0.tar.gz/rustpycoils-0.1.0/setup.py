from setuptools import setup
from setuptools_rust import Binding, RustExtension

setup(name='rustpycoils',
      author="J.D.R. Tommey",
      author_email="jake@tommey.co.uk",
      url='http://github.com/jdrtommey/rustpycoils/',
      description="Off-axis magnetic fields for coils and solenoids",
      long_description=open("README.md").read(),
      long_description_content_type='text/markdown',
      version="0.1.0",
      rust_extensions=[RustExtension('rustpycoils', 'Cargo.toml',  binding=Binding.PyO3)],
      test_suite="tests",
      license="MIT",
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities"],
      zip_safe=False)
