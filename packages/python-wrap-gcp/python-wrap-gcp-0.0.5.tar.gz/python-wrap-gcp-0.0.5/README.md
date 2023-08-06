## Wrap essential Google Cloud Platform functions to a python API

#### Set project credentials and list VM's by prefix
```python
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/Users/vadimskritskii/PycharmProjects/report/gcp/rock-embassy-279812-b252be8804df.json"
os.environ['FROM_LOCAL'] = 'false'
os.environ['GCP_BUCKET'] = 'bucket_name' 

from python_wrap_gcp import manage_instance
manage_instance.list_gcp_instances('INTERNAL_IP', prefix='cc-wiki')
```
Returns project VM's filtered by prefix as pandas.DataFrame
```text
NAME	ZONE	MACHINE_TYPE	PREEMPTIBLE	INTERNAL_IP	EXTERNAL_IP	STATUS
0	cc-wiki-1	us-central1-f	e2-medium	true	10.128.0.10	35.232.196.210	RUNNING
1	cc-wiki-2	us-central1-f	e2-medium	true	10.128.0.12	35.193.87.226	RUNNING
2	cc-wiki-3	us-central1-f	e2-medium	true	10.128.0.14	34.123.56.251	RUNNING
3	cc-wiki-4	us-central1-f	e2-medium	true	10.128.0.11	35.223.179.167	RUNNING
4	cc-wiki-5	us-central1-f	e2-medium	true	10.128.0.15	35.225.92.133	RUNNING
5	cc-wiki-6	us-central1-f	e2-medium	true	10.128.0.13	35.238.125.9	RUNNING```
```
##### Start all VM's by a prefix
```python
manage_instance.manage_gcp_instance(action='start', prefix='cc-wiki')
```
```text
[12:35:43.3]-[wrap_gcloud.py]-[wrap_gcloud_action]-[start: us-central1-f: cc-wiki-1,cc-wiki-2,cc-wiki-3,cc-wiki-4,cc-wiki-5,cc-wiki-6]-[I]-[9520cb]
```
#### Abstraction interface to read/write data either locally or on GCP
##### Load data from the bucket
```python
import json
from python_wrap_gcp import io
data = json.loads(io.emulate_open("gs://meely-inventory/data/context.json"))

# alternatively
from python_wrap_gcp.reload_data import load_gcs_file 
data, time_data_updated = load_gcs_file("gs://meely-inventory/data/context.json")
```
##### Save data locally
```python
import json, os
from python_wrap_gcp import io
os.environ['TO_LOCAL'] = 'true'

context = {"hello": "witam",
           "world": "świat"}
io.emulate_open("~/Desktop/context.json", method='wb', data=context)
```

##### Create VM's by creating a template & setting VM replicas
```python
from meely_crawl.docs import config
from python_wrap_gcp.configure_gcp import configure

configure_gcp = configure.Configure(config.Path, config.GCPConfig)
configure_gcp.set_up()
```