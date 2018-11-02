# cmip5-intake-datasets

This is a repo for collecting data resources for CMIP5. These may take the form of catalog files (YAML) of  directories on `Glade` which can be built into conda packages.

**NOTE:**

These datasets are directly accessible from NCAR's `Glade` **only**. 


## Install

    git clone https://github.com/NCAR/cmip5-intake-datasets
    cd cmip5-intake-datasets
    python setup.py install 

To test that everything is installed properly, run the following command:
```bash
$ cmip5-intake-cat-gen --help
Usage: cmip5-intake-cat-gen [OPTIONS]

Options:
  --config-data-file PATH  Configuration file containing data to feed in a
                           jinja template
  --template-file PATH     Template file
  --help                   Show this message and exit.
```


## How to generate intake catalog for cmip5 dataset

Examples of configuration, and template files are provided below:

### Step 1: Create a configuration file `config_data.yaml`

```yaml
module: intake_xarray
driver: netcdf
extra_args:
  engine: netcdf4
  chunks: {'time': 1}
root_path: /glade/collections/cmip/cmip5/
activity: output1
institution: NCAR
model: CCSM4
experiment: rcp26
frequency: mon
modeling_realm: atmos 
ensemble_member: r1i1p1
mip_table: Amon
variables:
  - tas
  - ci
  - tasmin
  - ta
  - psl
  - pr
  - tasmax
  - ts
  ```


### Step 2: Create a Template file `template.yaml`

```yaml
plugins:
  source:
    - module: {{ module }}

sources:
  {% for variable in variables%}
  {{ variable }}_{{ model }}_{{ experiment }}_{{ ensemble_member}}:
    description: Monthly - {{ variable }} data from the CMIP5
    driver: {{ driver }}
    args: 
      urlpath: "{{ root_path }}/{{ activity }}/{{ institution }}/{{ model }}/{{ experiment }}/{{ frequency }}/{{ modeling_realm }}/{{ mip_table }}/{{ ensemble_member }}/latest/{{ variable }}/{{ variable }}_{{ mip_table }}_{{ model }}*.nc"
      {% for key, item in extra_args.items() %}
      {{ key }}: {{ item }}
      {% endfor %}
    metadata:
      institution: {{ institution }}
      model: {{ model }}
      experiment: {{ experiment }}
      frequency: {{ frequency }}
      modeling_realm: {{ modeling_realm }}
      mip_table: {{ mip_table }}
      ensemble_member: {{ ensemble_member }}
  {% endfor %}
  ```


  ## Accessing the data 

```python
In [1]: import intake

In [2]: catalog = '/glade/work/abanihi/devel/pangeo/cmip5-intake-datasets/catalog.yaml'

In [3]: cat = intake.Catalog(catalog)

In [4]: ta_dset = cat.ta_CCSM4_rcp26_r1i1p1.to_dask()

In [5]: ta_dset
Out[5]:
<xarray.Dataset>
Dimensions:    (bnds: 2, lat: 382, lon: 288, plev: 17, time: 3540)
Coordinates:
  * lat        (lat) float64 -90.0 -89.06 -89.06 -88.12 ... 89.06 89.06 90.0
  * plev       (plev) float64 1e+05 9.25e+04 8.5e+04 7e+04 ... 3e+03 2e+03 1e+03
  * lon        (lon) float64 0.0 1.25 2.5 3.75 5.0 ... 355.0 356.2 357.5 358.8
  * time       (time) object 2006-01-16T12:00:00 ... 2300-12-16 12:00:00
Dimensions without coordinates: bnds
Data variables:
    time_bnds  (time, bnds) float64 dask.array<shape=(3540, 2), chunksize=(1, 2)>
    lat_bnds   (time, lat, bnds) float64 dask.array<shape=(3540, 382, 2), chunksize=(480, 382, 2)>
    lon_bnds   (time, lon, bnds) float64 dask.array<shape=(3540, 288, 2), chunksize=(480, 288, 2)>
    ta         (time, plev, lat, lon) float32 dask.array<shape=(3540, 17, 382, 288), chunksize=(1, 17, 382, 288)>
Attributes:
    institution:                  NCAR (National Center for Atmospheric Resea...
    institute_id:                 NCAR
    experiment_id:                rcp26
    source:                       CCSM4
    model_id:                     CCSM4
    forcing:                      Sl GHG Vl SS Ds SA BC MD OC Oz AA
    parent_experiment_id:         historical
    parent_experiment_rip:        r1i1p1
    branch_time:                  2005.0
    contact:                      cesm_data@ucar.edu
    references:                   Gent P. R., et.al. 2011: The Community Clim...
    initialization_method:        1
    physics_version:              1
    tracking_id:                  01046a60-720d-4da8-a38b-0720d9d6d665
    acknowledgements:             The CESM project is supported by the Nation...
    cesm_casename:                b40.rcp2_6.1deg.001
    cesm_repotag:                 ccsm4_0_beta49
    cesm_compset:                 BRCP26CN
    resolution:                   f09_g16 (0.9x1.25_gx1v6)
    forcing_note:                 Additional information on the external forc...
    processed_by:                 strandwg on copper.cgd.ucar.edu at 20111105...
    processing_code_information:  Last Changed Rev: 443 Last Changed Date: 20...
    product:                      output
    experiment:                   RCP2.6
    frequency:                    mon
    creation_date:                2011-11-05T17:37:02Z
    history:                      2011-11-05T17:37:02Z CMOR rewrote data to c...
    Conventions:                  CF-1.4
    project_id:                   CMIP5
    table_id:                     Table Amon (26 July 2011) 976b7fd1d9e1be31d...
    title:                        CCSM4 model output prepared for CMIP5 RCP2.6
    parent_experiment:            historical
    modeling_realm:               atmos
    realization:                  1
    cmor_version:                 2.7.1
```