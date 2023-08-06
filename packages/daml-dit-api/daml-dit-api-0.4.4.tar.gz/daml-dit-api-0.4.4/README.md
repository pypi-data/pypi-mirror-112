daml-dit-api
====

API definitions for DIT packages to be hosted in Daml Hub. This mainly
contains the [type definitions](daml_dit_api/package_metadata.py)
for the format of the `dabl-meta.yaml` file at the root of each DIT file.

DIT files are also used to contain integrations loaded and run by Daml
Hub. This repository also contains documentation (in this `README`)
describing the runtime environment that Daml Hub provides to
integrations.

# Package Metadata

At their core, DIT files are [ZIP archives](https://en.wikipedia.org/wiki/Zip_(file_format))
that follow a specific set of conventions regarding their content. The
most important of these conventions is the presence of a YAML metadata
file at the root of the archive and named `dabl-meta.yaml`. This
metadata file contains catalog information describing the contents of
the DIT, as well as any packaging details needed to successfully
deploy a DIT file into Daml Hub. An example of a deployment instruction is
a _subdeployment_. A subdeployment instructs Daml Hub to deploy a specific
subfile within the DIT file. A DIT file that contains an embedded DAR
file could use a subdeployment to ensure that the embedded DAR file is
deployed to the ledger when the DIT is deployed. In this way, a DIT
file composed of multiple artifacts (DARs, Bots, UI's, etc.) can be
constructed to deploy a set of artifacts to a single ledger in a
single action.

# Integrations

Integrations are a special case of DIT file that are augmented with
the ability to run as an executable within a Daml Hub cluster. This is
done by packaging Python [DAZL bot](https://github.com/digital-asset/dazl-client)
code into an [executable ZIP](https://docs.python.org/3/library/zipapp.html)
using [PEX](https://github.com/pantsbuild/pex) and augmenting tha
resulting file with the metadata and other resources needed to make it
a correctly formed DIT file.

Logically speaking, Daml Hub integrations are DAZL bots packaged with
information needed to fit them into the Daml Hub runtime and user
interface. The major functional contrast between a Daml Hub integration
and a Python Bot is that the integration has the external network
access needed to connect to an outside system and the Python Bot does
not. Due to the security implications of running within Daml Hub with
external network access, integrations can only be deployed with the
approval of DA staff.

## Developing Integrations

The easiest way to develop an integration for Daml Hub is to use the
[framework library](https://github.com/digital-asset/daml-dit-if)
and [`ddit` build tool](https://github.com/digital-asset/daml-dit-ddit).
The integration framework presents a Python API closely related to the
DAZL bot api and ensures that integrations follow the conventions
required to integrate into Daml Hub.

_Unless you know exactly what you are doing and why you are doing it,
use the framework._

## The Integration Runtime Environment

By convention, integrations accept a number of environment variables
that specify key paramaters.  Integrations built with the framework
use defaults for these variables that connect to a default locally
configured sandbox instance.

Variables provided by Daml Hub include the following:

| Variable | Default | Purpose |
|----------|---------|---------|
| `DAML_LEDGER_URL` | `http://localhost:6865` | Address of local ledger gRPC API |
| `DABL_HEALTH_PORT` | 8089 | Port for HTTP endpoint. (Used for both liveness/readiness and webhooks) |
| `DABL_JWKS_URL` | | HTTP URL for JWKS Repository |
| `DABL_INTEGRATION_METADATA_PATH` | 'int_args.yaml' | Path to local metadata file |
| `DABL_INTEGRATION_TYPE_ID` | | Type ID for the specific integration within the DIT to run |
| `DABL_LEDGER_PARTY` | | Party identifier for network connection |
| `DABL_LOG_LEVEL` | 0 | Log verbosity level - 0 up to 50, inclusive. |

(Note that for legacy reasons, the ledger URL is also available under
the `DABL_LEDGER_URL` environment variable.)

## Logging

DABL integrations use the default Python logging package, and the
framework provides specific support for controlling log level at
runtime. To integrate properly with this logic, it is important that
integrations use the `integration` logger. This logger is switched from
`INFO` level to `DEBUG` level at a `DABL_LOG_LEVEL` setting of 10 or above.

The preferred way of creating an integration logger is via the
`getIntegrationLogger` function in the API package.
