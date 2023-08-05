import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="NlpHub", 
    version="1.0.0",
    author="Muhammad Shahid Sharif",
    author_email="chshahidhamdam@gmail.com",
    description="A wrapper around Spacy, NLTK and uses some other libraries to perform Simple NLP tasks with less code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shahid017/NlpHub",
    packages=['NlpHub'],
    install_requires = ['spacy',
'nltk',
'sklearn',
'textblob',
'spacy-langdetect',
'spacy_readability',
'pandas',
'wordcloud',
'matplotlib',
'pdfminer'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
