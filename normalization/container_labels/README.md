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
Change the "input_dir" variable in ```replace_plural_labels.py``` to wherever your own input directory is, then run the script.