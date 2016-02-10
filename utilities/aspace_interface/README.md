#PySpace
A simple python interface for the ArchivesSpace API

##Requirements

* [Requests](https://github.com/kennethreitz/requests)
* [tqdm](https://github.com/noamraph/tqdm)

##Usage

First, make a pyspace object, which will handle all the connection details for you. To tailor it to your specific ASpace setup, you'll need to supply some info, like the host name, repository number, and login details:

```python
from pyspace import Pyspace

pyspace = Pyspace(host="http://localhost:8089", username="admin", password="admin", repository="2")
```

From there you can call any of pyspace's functions:

####Switching repositories
You can move to any repository if you know its ASpace number with the following:
```python
pyspace.change_repository(repository_number)
```

####Convert EAD file to json
Requires the json_from_format plugin. Returns a python json object
```python
ead_json = pyspace.ead_to_json(path_to_ead_file)
```

####Add new resources from json
Takes a json representation of an EAD file and posts it to ASpace
```python
pyspace.add_ead(ead_json)
```

####Add new accession from json
```python
pyspace.add_accession(json_data)
```

####Add new agent
Allows the addition of new agents to ASpace.

Can add people:
```python
pyspace.add_person(json_data)
```

corporations:
```python
pyspace.add_corporation(json_data)
```

or families:
```python
pyspace.add_family(json_data)
```

There is also a more general interface to add any agent, which requires an agent type string:
```python
pyspace.add_agent(json_data, agent_type)
```

Valid type strings include ```families```, ```corporate_entities```, and ```people```.

####Retrieving ASpace IDs
Allows the retrieval of all ASpace IDs of a specified object type. E.g.:
```python
accession_ids = pyspace.get_all_object_ids("accessions")
```
The following is a full list of valid object types that can be retrieved:
```
accessions
archival_objects
classification_terms
classifications
digital_object_components
digital_objects
events
groups
resources
```

####Removing ASpace objects
Given an object type and its ASpace ID, will delete that object:
```python
pyspace.delete_aspace_object("accessions", "125")
```

The object type values are limited to the same set of strings as above.

####Removing a single agent
Given an agent URI, will delete that agent:
```python
pyspace.delete_agent_by_uri('/agents/corporate_entities/103'
```

####Deleting all agents
If you want to purge all agents from a given ASpace installation, use the following:

```python
pyspace.delete_all_agents()
```

Note: this may take a while.