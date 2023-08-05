FunPDBe JSON Validator
======================

[![Build Status](https://travis-ci.com/PDBe-KB/funpdbe-validator.svg?branch=master)](https://travis-ci.com/PDBe-KB/funpdbe-validator)
[![codecov](https://codecov.io/gh/PDBe-KB/funpdbe-validator/branch/master/graph/badge.svg?token=MQMUUE5DJO)](https://codecov.io/gh/PDBe-KB/funpdbe-validator)
[![Maintainability](https://api.codeclimate.com/v1/badges/583ee28bcdc5d62a2b1e/maintainability)](https://codeclimate.com/github/PDBe-KB/funpdbe-validator/maintainability)

This Python3 client can be used for validating FunPDBe JSON files. It performs various sanity checks, and validates user JSONs against the FunPDBe schema.

For more information on FunPDBe is, visit https://funpdbe.org

Quick start
-----------

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Please note that the client is written in Python3, and the dependencies have to be installed accordingly (i.e. using pip3)!

### Installing

#### Checking out this repository from GitHub

```
$ git clone https://github.com/PDBe-KB/funpdbe-validator.git
$ cd funpdbe-validator
$ pip3 install -r requirements.txt
```

#### Installing with PIP

```
pip install funpdbe-validator
```

### Basic usage

This package contains two classes which handle the validation of FunPDBe JSON files.

* Validator()
* ResidueIndexes()

Basic example:
```
from funpdbe_validator.validator import Validator
from funpdbe_validator.residue_index import ResidueIndexes

def run():
    """
    Basic example of running the PDBe-KB/FunPDBe validator
    :return:
    """
    validator = Validator("name of the resource") # Same as in the JSON
    validator.load_schema()
    validator.load_json("/path/to/data.json")

    if validator.basic_checks() and validator.validate_against_schema():
        print("Passed data validations")
        residue_indexes = ResidueIndexes(validator.json_data)
        if residue_indexes.check_every_residue():
            print("Passed the index validation")
            return True
    return False


if __name__ == "__main__":
    run()
```
Using mmcif instead of PDBe-API for valiation:
ResidueIndexes class has optional arguments- 'mmcif_mode' and 'cif_file'. When mmcif_mode is set True, the validator uses given mmcif (set using cif_fie) for validation instead of PDBe-API.

```
def run(resource_name, json_path, mmcif_mode=False, cif_file =None):
    """
    Basic example of running the PDBe-KB/FunPDBe validator
    :return: None
    """
    validator = Validator(resource_name) # Same as in the JSON
    validator.load_schema()
    for json_file_path in glob.glob('%s*.json' % json_path):
        validator.load_json(json_file_path)
        if validator.basic_checks() and validator.validate_against_schema():
            print("Passed data validations for %s" % json_file_path)
            residue_indexes = ResidueIndexes(validator.json_data,mmcif_mode,cif_file)
            if residue_indexes.check_every_residue():
                print("Passed the index validation for %s" % json_file_path)
                return True
            else:
                print("Failed index validation for %s: %s" % (json_file_path, residue_indexes.mismatches))
        else:
            print("Failed data validations for %s: %s" % (json_file_path, validator.error_log))
    return False
```

### Using the "basic_run.py"

This script runs the validator for all the JSON files found at a specified path. **Note**: the path has to end with a /

```
python basic_run.py dataResourceName path/to/json/files/
```

### Using the Dockerized version

```
docker build --tag funpdbe-validator-basic .
docker run funpdbe-validator-basic dataResourceName path/to/json/files/
```

### Running the tests

Running tests for the client is performed simply by using
```
$ pytest tests
```

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/funpdbe-consortium/funpdbe-validator/tags).

## Authors

* **Mihaly Varadi** - *Initial work* - [mvaradi](https://github.com/mvaradi)

Special thanks to:
* Skoda Petr https://github.com/skodapetr
* Radoslav Krivak https://github.com/rdk

## License

This project is licensed under the EMBL-EBI License - see the [LICENSE](LICENSE) file for details