"""setup."""
import setuptools

setuptools.setup(
    name="duckduckgo_images_api",
    version="1.0.0",
    url="https://github.com/joeyism/duckduckgo-images-api",
    author="joeyism",
    description="DuckDuckGo Image Search Results - using Python !",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords="duckduckgo image api",
    license="MIT",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=['requests>=2.18.4',],
)
