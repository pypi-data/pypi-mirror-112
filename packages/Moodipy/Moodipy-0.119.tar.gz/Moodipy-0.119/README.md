# Moodipy
Uses sentiment analysis to create a playlist on spotify that matches someone's mood and also predict songs to rise in popularity.



## Installation instructions

### Package name for PIP installation:
* pip install Moodipy==0.118
### Executable command:
* Moodipy
### Link to repository:
* https://github.com/dianas11xx/Moodify

### App Requirements
* In our current prototype, the user needs to have a spotify premium account and have some liked songs in their library.

### Required packages commands if the distribution is not found in PYPI: 
* screeninfo:
  * pip install screeninfo
* spotipy
  * pip install spotipy
* urllib3==1.26.6:
  * pip install urllib3 --upgrade
* requests>=2.25.0
  *  pip install requests --upgrade
* nltk:
  * pip install nltk
  * python3 -m nltk.downloader punkt
  * python3 -m nltk.downloader stopwords
  * python3 -m nltk.downloader averaged_perceptron_tagger
  * python3 -m nltk.downloader wordnet
* PyQt5:
  * pip3 install --user pyqt5
  * sudo apt-get install pyqt5-dev-tools
  * sudo apt-get install qttools5-dev-tools