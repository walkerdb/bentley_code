#Container label cleanup
Normalizes all ```label``` attributes on container tags from their plural to their singular forms

eg 

```xml
<container label="Boxes">24</container>
```

becomes

```xml
<container label="Box">24</container>
```

##Requirements

* [lxml](http://lxml.de/)
* [tqdm](https://github.com/noamraph/tqdm)

##Usage
Just run ```replace_plural_labels.py```