# coho-spider

This is a scraper written by @haaroon and @rachchan that can be used to scrape data from companies house. 

It uses python and scrapy.

You need to set the API KEY to the API_KEY_COMPANIES_HOUSE variable inside tutorial/spiders/cohoPscSpider.py

You also need to set the companies numbers without headers file. I have added a list of companies. 

We have a list of companies but it may not be upto date. 

You can get an api from the companies house website. 

You can also contact companies house directly, their support and developer teams are extremely friendly and 
can get you direct access to bulk read only data. 

> pip install scrapy
> cd tutorial
> scrapy crawl persons-with-significant-control

This will produce a `data` folder that contains a folders of companies, inside with a person of significant control


# license 

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.