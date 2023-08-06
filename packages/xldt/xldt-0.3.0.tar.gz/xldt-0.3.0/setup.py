import setuptools

xldt_description = None

with open("README.md", "r", encoding="utf-8") as f:
    xldt_description = f.read()

xldt_keywords = ["python", "excel", "date", "time"]

setuptools.setup(name="xldt",
    version="0.3.0",
    author="Vlad Tudorache",
    author_email="tudorache.vlad@gmail.com",
    description="Excel-compatible date and time functions.",
    long_description=xldt_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vtudorache/xldt",
    classifiers=[
        "Programming Language :: C",
        "License :: OSI Approved :: MIT License"
    ],
    keywords = " ".join(xldt_keywords),
    ext_modules=[setuptools.Extension("xldt", ["src/xldt.c"])],
    python_requires=">=3.6"
)
