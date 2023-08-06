# Import our newly installed setuptools package.
import setuptools

# Opens our README.md and assigns it to long_description.
with open("README.md", "r") as fh:
	long_description = fh.read()



# Function that takes several arguments. It assigns these values to our package.
setuptools.setup(
	# Distribution name the package. Name must be unique so adding your username at the end is common.
	name="pxtextmining",
	# Version number of your package. Semantic versioning is commonly used.
	version="0.2.5",
	# Author name.
	author="Andreas D Soteriades",
	# Author's email address.
	author_email="andreas.soteriades@nottshc.nhs.uk",
	# Short description that will show on the PyPi page.
	description="Text Classification of Patient Experience feedback",
	# Long description that will display on the PyPi page. Uses the repo's README.md to populate this.
	long_description=long_description,
	# Defines the content type that the long_description is using.
	long_description_content_type="text/markdown",
	# The URL that represents the homepage of the project. Most projects link to the repo.
	url="https://github.com/CDU-data-science-team/pxtextmining",
	# Finds all packages within in the project and combines them into the distribution together.
	packages=setuptools.find_packages(),
	# requirements or dependencies that will be installed alongside your package when the user installs it via pip.
	install_requires=[
    "blis==0.7.4", 
    "catalogue==1.0.0", 
    "certifi==2021.5.30", 
    "chardet==4.0.0", 
    "click==8.0.1", 
    "cycler==0.10.0", 
    "cymem==2.0.5", 
    "emojis==0.6.0", 
#    "en_core_web_lg @ https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-2.3.1/en_core_web_lg-2.3.1.tar.gz", 
#    "en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz", 
    "idna==2.10", 
    "imbalanced-learn==0.7.0", 
    "joblib==1.0.1", 
    "kiwisolver==1.3.1", 
    "matplotlib==3.3.2", 
    "murmurhash==1.0.5", 
    "mysql-connector-python==8.0.23", 
    "nltk==3.5", 
    "numpy==1.20.2", 
    "pandas==1.2.3", 
    "pickleshare==0.7.5", 
    "Pillow==8.2.0", 
    "plac==1.1.3", 
    "preshed==3.0.5", 
    "protobuf==3.17.2", 
    "pyparsing==2.4.7", 
    "python-dateutil==2.8.1", 
    "pytz==2021.1", 
    "regex==2021.4.4", 
    "requests==2.25.1", 
    "scikit-learn==0.23.2", 
    "scipy==1.6.3", 
    "seaborn==0.11.0", 
    "six==1.16.0", 
    "spacy==2.3.5", 
    "SQLAlchemy==1.3.23", 
    "srsly==1.0.5", 
    "textblob==0.15.3", 
    "thinc==7.4.5", 
    "threadpoolctl==2.1.0", 
    "tqdm==4.61.0", 
    "urllib3==1.26.5", 
    "vaderSentiment==3.3.2", 
    "wasabi==0.8.2"
    ],
    dependency_links=[
        "https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-2.3.1/en_core_web_lg-2.3.1.tar.gz", 
        "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz"
    ],
	# Gives pip some metadata about the package. Also displays on the PyPi page.
	classifiers=[
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	# The version of Python that is required.
	python_requires='>=3.6',
)
