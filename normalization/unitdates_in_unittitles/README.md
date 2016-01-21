#Intelligently removing unitdates from unittitles

Archivesspace has a bad habit of blindy moving all unitdate tags inside of unittitles to the outside, without any consideration for context that might be lost. For example, if the following is run through the ASpace EAD importer:

```xml
<unittitle>Campaigns <unitdate>1972-1975</unitdate> (including <unitdate>1974</unitdate> Charter Revision)</unittitle>
```

it becomes

```xml
<unittitle>Campaigns (including Charter Revision)</unittitle>
<unitdate>1972-1975</unitdate>
<unitdate>1974</unitdate>
```

What do these unitdates apply to? No one knows!

This script intelligently determines cases where removing unitdates from unittitles will possibly result in a loss of essential context. If it finds a likely candidate, it makes copies of the current unitdate tags, places them after the unittitle to appease ASpace, then removes the unitdate tags from the unittitle while leaving their respective texts intact. So the above example would be transformed into the following:

```xml
<unittitle>Campaigns 1972-1975 (including 1974 Charter Revision)</unittitle>
<unitdate>1972-1975</unitdate>
<unitdate>1974</unitdate>
```

It also pre-emptively removes all unitdates from unittitles for all other cases (when context will not be lost) just as ASpace would have done it, except with some slightly more intelligent cleanup routines (largely removing redundant punctuation leftover from the removal process).

##Requirements

* [lxml](http://lxml.de/)
* [tqdm](https://github.com/noamraph/tqdm)

##Usage
Change the input and output directory variables in ```unitdates_unittitles_fix.py``` to fit your own needs, then run the script.