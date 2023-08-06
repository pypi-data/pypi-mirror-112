# AnaTools

## Project Description
Anatools is a python package with modules for developing with the Ana Platform from Rendered.AI.
With AnaTools you can generate and access synthetic datasets, and much more!
```python
>>> import anatools
>>> ana = anatools.AnaClient()
'Enter your credentials for Ana.'
'email:' example@rendered.ai
'password:' ***************
>>> ana.get_channels()
['mychannel1', 'mychannel2']
>>> graphs = ana.get_graphs()
>>> datasets = ana.get_datasets()
```

<br /><br />
## Install the AnaTools Package
#### (Optional) Create a new Conda Environment
1. Install conda for your operating system: https://www.anaconda.com/products/individual.
2. Create a new conda environment and activate it.
3. Install anatools from the Python Package Index.
```sh
$ conda create -n renderedai python=3.7
$ conda activate renderedai
```
#### Install AnaTools to the Python Environment
1. Install AnaTools from the Python Package Index.
```sh
$ pip install anatools
```
#### Dependencies
The anatools package requires python 3.6 or higher and has dependencies on the following packages:

| Package | Description |
|-|-|
| pyrebase| A python wrapper for Google Firebase API. |
| jwt | A python library for encoding and decoding JSON web tokens. |
| keyring | A python library for storing and accessing passwords securely. |
| docker | A python library for the Docker Engine API. |
| sphinx | A python documentation generator. |
| pytest | A python testing framework. |
| pyyaml | A python YAML parser and emitter. |

If you have any questions or comments, contact Rendered.AI at info@rendered.ai.

<br /><br />
## Quickstart Guide
#### What is Ana?
Ana is a synthetic dataset generation tool where graphs describe what and how synthetic datasets are generated.

| Terms | Definitions |
|-|-|
| workspace | A workspace is a collection of data used for a particular use-case, for example workspaces can be used to organize data for different projects.
| dataset | A dataset is a collection of data, for many use-cases these are images with text-based annotation files. |
| graph | A graph is defined by nodes and links, it describes the what and the how a dataset is generated. |
| node | A node can be described as an executable block of code, it has inputs and runs some algorithm to generate outputs. |
| link | A link is used to transfer data from the output of one node, to the input of other nodes. |
| channel | A channel is a collection of nodes, it is used to limit the scope of what is possible to generate in a dataset (like content from a tv channel). |

#### How do you use Ana?
Ana creates synthetic datasets by processing a graph, so we will need to create our Ana client, create a graph, then create a dataset.
1. Execute the python command line, create a client and login to Ana.
In this example we are instantiating a client with no workspace or environment variables, so it is setting our default workspace.
To access the tool, you will need to use your email and password for https://deckard.rendered.ai.
```python
>>> import anatools
>>> ana = anatools.AnaClient()
'Enter your credentials for Ana.'
'email:' example@rendered.ai
'password:' ***************
```
2. Create a graph file called 'graph.yml' with the code below. 
We are defining a simplistic graph for this example with multiple cubes dropped into a container.
Graphs are usually stored in json or yaml format, but read into a python dictionary to be passed to the API.
```yaml
nodes:

  Cube:
    class: CubeGenerator

  ObjectPlacement:
    class: RandomPlacement
    inputs: 
      object_generator: {$link: [Cube, object_generator]}
      object_number: '5'

  Container:
    class: ContainerGenerator

  DropObjects:
    class: DropObjectsNode
    inputs:
      objects: {$link: [ObjectPlacement, objects]}
      container_generator: {$link: [Container, object_generator]}
      
  Render:
    class: RenderNode
    inputs:
      frame_number: 150
      target_object: {$link: [DropObjects, target_object]}
      annotated_objects: {$link: [DropObjects, annotated_objects]}
```
3. Create a graph using the client.
To create a new graph, we load the graph defined above into a python dictionary using the yaml python package.
Then we create a graph using the client, this graph is being named 'testgraph' and is using the 'example' channel.
The client will return a graphid so we can reference this graph later.
```python
>>> import yaml
>>> with open('graph.yml') as graphfile:
>>>     graph = yaml.safe_load(graphfile)
>>> graphid = ana.create_graph(name='testgraph',channel='example',graph=graph)
>>> graphid
'e175a44e-23a5-11eb-adc1-0242ac120002'
```
4. Create a dataset using the client.
Using the graphid, we can create a new job to generate a dataset.

The client will return a datasetid that can be used for reference later.
``` python
>>> datasetid = ana.create_dataset(name='testdataset',graphid=graphid,interpretations='10',priority='1',seed='1',description='A simple dataset with cubes in a container.')
>>> datasetid
'ce66e81c-23a6-11eb-adc1-0242ac120002 '
```