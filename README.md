# Coho Spider

This is a scraper written by @haaroon and @rachchan that can be used to scrape data from Companies House. 

## Requirements
- Python >= 3.7
- Scrapy >= 2.8.0
- Companies House Developer Hub Account/REST API Key 
- List of Company Numbers from Companies House to scrape (optional)

We have included a list of companies if you do not have any, but it may not be up to date. 

You can get an API key from the Companies House website. 

You can also contact [Companies House](https://forum.aws.chdev.org/) directly, their support and developer teams are extremely friendly and can get you direct access to bulk read only data. 

## Installation Guide

First, open up a new terminal and install our scraper.
```
pip install -i https://test.pypi.org/simple/ cohospider
```

Next, open up your python terminal of choice, pick a spider to use and enter the following commands.

### Scraping Persons With Significant Control 
If you would like to obtain JSON data on a company's Persons With Significant Control, you can follow the following commands:

```
from spiders import CohoPscSpiderRun
```
*With default Company data*
```
psc_runner = CohoPscSpiderRun(key="INSERT_API_KEY_HERE")
```
*OR with your own company data*
```
psc_runner = CohoPscSpiderRun(key="INSERT_API_KEY_HERE", company_numbers=[COMPANY_NUMBER1, COMPANY_NUMBER2, etc..])
```
```
psc_runner.start()
```

The output will follow this JSON format:
https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/resources/list?v=latest

### Scraping Directors

If you would like to obtain JSON data on a company's Directors, you can follow the following commands:

```
from spiders import CohoOfficerSpiderRun
```
*With default Company data*
```
officer_runner = CohoOfficerSpiderRun(key="INSERT_API_KEY_HERE")
```
*OR with your own company data*
```
officer_runner = CohoOfficerSpiderRun(key="INSERT_API_KEY_HERE", company_numbers=[COMPANY_NUMBER1, COMPANY_NUMBER2, etc..])
```
```
officer_runner.start()
```

The output will follow this JSON format:
https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/resources/officerlist?v=latest

### Scraping for our example notebook

If you are following our example notebook/blog on Companies House in Raphtory, you will need to use our barbara-spider:

```
from spiders import BarbaraSpiderRun
```
```
barbara_runner = CohoOfficerSpiderRun(key="INSERT_API_KEY_HERE")
```
```
barbara_runner.start()
```
The output will follow this JSON format:
https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/resources/officerlist?v=latest



All these runners produce a `data` folder in your root directory, where you can find all your JSON data, ready to be used in Raphtory for analysis.

# License 

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.