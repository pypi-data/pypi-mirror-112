
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="googleanswer",
    version="1.2",
    author="Sanat Garg",
    author_email="sanatgarg11@gmail.com",
    description="The supreme Google Search API",
    long_description="Google Search API is a real-time API to access Google search results. We handle proxies, solve captchas, and parse all rich structured data for you.",
    long_description_content_type="text/markdown",
    url="https://github.com/sanat-garg/google_search",
    project_urls={"Google Search": "https://github.com/sanat-garg/google_search",},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests'],
    packages=['googleanswer'],
    python_requires=">=3.0",
)