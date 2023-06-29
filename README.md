# Novel Scraper
A tool build to scrape sites presenting webnovels as a webpage,
with flexibility in mind.

## Table of contents
- [Using the program](#Usage)
- [Getting the needed data to filter the elements](#Preparation)
- [An example](#Example)

## Usage:
### Installation:
You only need to download the main.py script
#### Needed Packages:
- requests
- BeautifulSoup4
- time
- json
- os
### Preparation:
Before executing the script, you need to go to the site of choice and open the inspector.
There, you will have to look for the following elements:
- The url of the first chapter (or whichever chapter was last downloaded)
- The base url to which the (mostly relative links are added)
- The element containing the title
- the link which directs to the next site
- The element(s) that contain(s) the text

### Filters for the needed elements
You can use any of these to get an element in the page.
- class name
- id name
- element name

Using either the id or class is recommended over the element name though, as the whole DOM will be searched.

You can also use multiple key-value pairs for in example the link, meaning you can check 
for multiple variants with just one more line in the .json file

### Example
For example, [this novel on readnovelfull.com](https://readnovelfull.me/world-domination-system/chapter-c-1-power-levels-and-abbreviations/).

#### The .json file will look something like this:
```json
{
  "last": "/world-domination-system/chapter-c-1-power-levels-and-abbreviations/",
  "last_write_to": null,
  "base_url": "https://readnovelfull.me",
  "chapters_done": 0,
  "next_page_finder": {
    "id1": "next_chap"
  },
  "title_finder": {
    "class1": "chr-text"
  },
  "text_finder": {
    "find_all": true,
    "element1": "p"
  },
  "skip": true
}
```

#### "last"
The **"last"** chapter will allow the scraper to start off from where it left. It's important to note that I programmed this under the impression that all novel websites use relative links. <br>
Because of that, the last chapter has to be a relative link, i.e. "/world-domination-system/chapter-1-daneel/". The rest of the url will be created with the base_url parameter.
You have to have a "/" at the beginning because without it the program will fail

#### "last_write_to"
The **"last_write_to"** can get set to `null`, because we didn't write to any file yet and
the program will create new ones automatically.

#### "base_url"
The previously mentioned **"base_url"** in our case is "https://readnovelfull.me", as all of the
links to the next chapter are relative (i.e. "/world-domination-system/chapter-1-daneel/")

#### "chapters_done"
**"chapters_done"** is used to split the chapters to files containing 100 chapters each.
You have to set this to `0`, as it checks whether the chapters are divisible
by 100.

#### "next_page_finder"
The element containing the link that directs to the next chapter is:
<br>`<a class="btn btn-success" href="/world-domination-system/chapter-1-daneel/" title="Chapter 1 Daneel" id="next_chap">...</a>`
<br> To now filter that in the program, you have to grab one of these:
- class name
- id name
- element name

Using either the id or class is recommended over the element name though, as the whole DOM will be searched.
<br>Because there are multiple elements with the class "btn" or "btn-success", we will use the id, which is "next_chap".

#### "title_finder"
The element containing the title is: 
<br>`<span class="chr-text">Chapter c-1 Power Levels And Abbreviations</span>`
<br>It has a class name, "chr-text", so we will use that for the filter.

#### "text_finder"
The last thing we need is the elements that contain the text.
<br>These are a lot of `<p>`'s, so we'll grab those and add a key with the "find_all" key set to true.

#### "skip"
The last thing in our json file is **"skip"**, which you just have to set to false, as it is
used to download new chapters and not download the last one again.
