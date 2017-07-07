
## clsearch

An AWS Lambda oriented tool for watching craigslist for particular items and notifying you.


### How to Use

* Perform the desired search in Craigslist, then copy/paste the search query string into the `search` attribute.  Sample:

From the following URL:

https://seattle.craigslist.org/search/cta?query=audi+s4&srchType=T&auto_paint=2

Copy the string after `search/`, e.g.
`cta?query=audi+s4&srchType=T&auto_paint=2`

<< insert gif of CL URL query string copy/pasta >>

* Specify the search scope (everywhere, just your state, list of cities)
* Use apex to create your function in AWS lamdba and start running, or use the included Terraform.


### Running locally

Use [run_lambda](https://pypi.python.org/pypi/run-lambda) to invoke locally (assuming AWS credentials are already configured):

```sh
run_lambda -f handler functions/clsearch/main.py event.json
```
