## maelstrom-nogwd

A CliMetLab dataset plugin for the dataset maelstrom-nogwd. 


Features
--------

In this README is a description of how to get the maelstrom-nogwd.

## Dataset description
Contains the input/output dataset for learning non-orographic 
gravity wave drag, as described in https://arxiv.org/abs/2101.08195

Data is grouped by forecast start date.

Data has been preprocessed into inputs "x" and outputs "y". 
"x" contains vertical profiles of winds & temperature plus surface values
of pressure and geopotential.
"y" contains the the wind increments due to parametrised non-orographic
gravity wave drag. The machine learning task is to predict y given x.
Unlike many ML tasks within the field of weather and climate, this task
can be predicted independently for each column of atmosphere.

## Using climetlab to access the data
Data can be accessed either by forecast start-date or dataset type.
With neither argument provided, the first file is loaded, corresponding
to 2015-01-01 (the tier-1 dataset). Incorrect dates will be flagged.
Other dataset types are "training", "validation" & "testing" corresponding
to the date groups outlined in https://arxiv.org/abs/2101.08195


The climetlab python package allows easy access to the data with a few lines of code such as:
```

!pip install climetlab climetlab_maelstrom_nogwd
import climetlab as cml
cmlds = cml.load_dataset("maelstrom-nogwd", date='2015-01-01')
ds = cmlds.to_xarray()
#or
cmlds = cml.load_dataset("maelstrom-nogwd", dataset='training')
ds = cmlds.to_xarray()
```

See notebooks/demo_nogwd.ipynb for a short tutorial.
