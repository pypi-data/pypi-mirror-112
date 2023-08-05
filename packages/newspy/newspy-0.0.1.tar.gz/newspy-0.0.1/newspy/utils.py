import json
import re
import sys
import time
from urllib.parse import unquote

import pandas as pd
import requests
import unidecode
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from newspaper import Article
from newsplease import NewsPlease
from requests import get
