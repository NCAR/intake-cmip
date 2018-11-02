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
    description: {{ description }}
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



### Step 3: Generate catalog YAML file using `cmip-intake-catp-gen` command

    $ cmip5-intake-cat-gen --config-data-file config_data.yaml --template-file template.yaml

The output of this command, is a YAML file `catalog.yaml` that contains:

```yaml
plugins:
  source:
    - module: intake_xarray

sources:
  tas_CCSM4_rcp26_r1i1p1:
    description: 
    driver: netcdf
    args: 
      urlpath: "/glade/collections/cmip/cmip5//output1/NCAR/CCSM4/rcp26/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_CCSM4*.nc"
      engine: netcdf4
      chunks: {'time': 1}
    metadata:
      institution: NCAR
      model: CCSM4
      experiment: rcp26
      frequency: mon
      modeling_realm: atmos
      mip_table: Amon
      ensemble_member: r1i1p1
  ci_CCSM4_rcp26_r1i1p1:
    description: 
    driver: netcdf
    args: 
      urlpath: "/glade/collections/cmip/cmip5//output1/NCAR/CCSM4/rcp26/mon/atmos/Amon/r1i1p1/latest/ci/ci_Amon_CCSM4*.nc"
      engine: netcdf4
      chunks: {'time': 1}
    metadata:
      institution: NCAR
      model: CCSM4
      experiment: rcp26
      frequency: mon
      modeling_realm: atmos
      mip_table: Amon
      ensemble_member: r1i1p1
  tasmin_CCSM4_rcp26_r1i1p1:
    description: 
    driver: netcdf
    args: 
      urlpath: "/glade/collections/cmip/cmip5//output1/NCAR/CCSM4/rcp26/mon/atmos/Amon/r1i1p1/latest/tasmin/tasmin_Amon_CCSM4*.nc"
      engine: netcdf4
      chunks: {'time': 1}
    metadata:
      institution: NCAR
      model: CCSM4
      experiment: rcp26
      frequency: mon
      modeling_realm: atmos
      mip_table: Amon
      ensemble_member: r1i1p1
  ta_CCSM4_rcp26_r1i1p1:
    description: 
    driver: netcdf
    args: 
      urlpath: "/glade/collections/cmip/cmip5//output1/NCAR/CCSM4/rcp26/mon/atmos/Amon/r1i1p1/latest/ta/ta_Amon_CCSM4*.nc"
      engine: netcdf4
      chunks: {'time': 1}
    metadata:
      institution: NCAR
      model: CCSM4
      experiment: rcp26
      frequency: mon
      modeling_realm: atmos
      mip_table: Amon
      ensemble_member: r1i1p1
```

