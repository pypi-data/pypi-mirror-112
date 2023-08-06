
# fathomdata

Python package to make interacting with life sciences manufacturing data quick and intuitive. Getting the data should be the easy part.

## Usage
---

### API setup
```
import fathomdata as fd

fd.set_api_key('xxx')
```

### Get structured dataframes for documents that have been ingested
```
documents = fd.available_documents()
for index, row in documents.iterrows():
    document = fd.get_document(row['DocumentId'])
    print(document.get_materials_df())
    print(document.get_steps_df())
    print(document.get_parameters_df())
```

### Ingest a new document into the dataset
```
new_document_id = fd.ingest_document(path="/path/to/document.pdf")
```

### Create control charts for continuous process validation
```
import matplotlib.pyplot as plt

document_ids = documents['DocumentId'].tolist()

actuals = fd.get_parameter_actuals_across_documents(document_ids)
print(actuals)

titer_actuals = actuals.loc['Titer']
yield_actuals = actuals.loc['Yield']

first_document_params_df = fd.get_document(document_ids[0]).get_parameters_df()

titer_operating_limits = {
    'lower': first_document_params_df.at['Titer', 'Lower Operating Limit'],
    'upper': first_document_params_df.at['Titer', 'Upper Operating Limit']
}

yield_operating_limits = {
    'lower': first_document_params_df.at['Yield', 'Lower Operating Limit'],
    'upper': first_document_params_df.at['Yield', 'Upper Operating Limit']
}

fig, axes = plt.subplots(2, 1, sharex=True, figsize=(8,12))
titer_control_chart = fd.create_control_chart(axes[0], titer_actuals, titer_operating_limits['lower'], titer_operating_limits['upper'])
yield_control_chart = fd.create_control_chart(axes[1], yield_actuals, yield_operating_limits['lower'], yield_operating_limits['upper'])
```
