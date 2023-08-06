import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt','r') as fr:
    requires = fr.read().split('\n')

setuptools.setup(
    # pip3 smoothie_diet ebook_pdf
    name="smoothie_diet ebook_pdf", # Replace with your own username
    version="9",
    author="smoothie diet ebook pdf",
    author_email="admin@xdiet.com",
    description="smoothie diet ebook pdf",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://tinyurl.com/smoothiedietebookpdf",
    project_urls={
        "Bug Tracker": "https://github.com/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=requires,
)
