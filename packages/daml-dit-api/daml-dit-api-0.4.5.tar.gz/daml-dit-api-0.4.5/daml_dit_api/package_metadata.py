import logging
import datetime
from dataclasses import dataclass, field, replace
from typing import Any, Dict, Optional, Sequence


TAG_EXPERIMENTAL = "experimental"


def _empty_tags() -> 'Sequence[str]':
    return list()


@dataclass(frozen=True)
class IntegrationTypeFieldInfo:
    id: str
    name: str
    description: str
    field_type: str
    help_url: 'Optional[str]' = None
    default_value: 'Optional[str]' = None
    required: 'Optional[bool]' = True
    tags: 'Sequence[str]' = field(default_factory=_empty_tags)
    field_context: 'Optional[str]' = None


@dataclass(frozen=True)
class IntegrationTypeInfo:
    artifact_hash: 'Optional[str]'
    id: str
    name: str
    description: str
    fields: 'Sequence[IntegrationTypeFieldInfo]'
    entrypoint: str
    env_class: 'Optional[str]'
    runtime: 'Optional[str]' = None
    help_url: 'Optional[str]' = None
    instance_template: 'Optional[str]' = None
    tags: 'Sequence[str]' = field(default_factory=_empty_tags)


@dataclass(frozen=True)
class CatalogInfo:
    name: str
    version: str
    description: str
    release_date: 'Optional[datetime.date]'
    author: 'Optional[str]'
    url: 'Optional[str]'
    email: 'Optional[str]'
    license: 'Optional[str]'
    experimental: 'Optional[bool]'
    demo_url: 'Optional[str]'
    source_url: 'Optional[str]'
    tags: 'Sequence[str]' = field(default_factory=_empty_tags)
    short_description: 'Optional[str]' = None
    group_id: 'Optional[str]' = None
    icon_file: 'Optional[str]' = None
    dit_if_requirement: 'Optional[str]' = None


@dataclass(frozen=True)
class DamlModelInfo:
    name: str
    version: str
    main_package_id: str


# Key name used to identify DIT metadata bundled into daml.yaml
DIT_META_KEY_NAME = 'dit-meta'

# The original and current names of the DIT metadata subfile.
DABL_META_NAME = 'dabl-meta.yaml'
DIT_META_NAME = 'dit-meta.yaml'

# Lookup names for package metadata. Listed in search order.
DIT_META_NAMES = [ DIT_META_NAME, DABL_META_NAME ]

@dataclass(frozen=True)
class PackageMetadata:
    catalog: 'Optional[CatalogInfo]'
    subdeployments: 'Optional[Sequence[str]]'
    daml_model: 'Optional[DamlModelInfo]'
    integration_types: 'Optional[Sequence[IntegrationTypeInfo]]'

    # Deprecated in favor of integration_types
    integrations: 'Optional[Sequence[IntegrationTypeInfo]]'


def normalize_catalog(catalog: "CatalogInfo") -> "CatalogInfo":
    """
    Normalize catalog information into the most current representation
    of the given attributes.  As the catalog format has changed, there
    have come to be multiple ways that certain fields can be represented.
    Calling this function ensures that the catalog is represented in the
    most current way.
    """

    updates = {}  # type: Dict[str, Any]

    # Legacy integrations (before September 2020) store the
    # short_description in the name and do not have a name
    # specified in metadata. This ensures that these integations
    # get a short description.
    if catalog.short_description is None:
        updates["short_description"] = catalog.name

    # The experimental nature of a DIT can be stored either
    # as a tag or via the experimental flag. This ensures
    # that both representations are consistent with each other.
    experimental = catalog.experimental or (TAG_EXPERIMENTAL in catalog.tags)

    updates["experimental"] = experimental

    if experimental and not (TAG_EXPERIMENTAL in catalog.tags):
        updates["tags"] = list(catalog.tags) + [TAG_EXPERIMENTAL]

    return replace(catalog, **updates)


def normalize_package_metadata(metadata: 'PackageMetadata') -> 'PackageMetadata':
    updates = {}  # type: Dict[str, Any]

    if metadata.catalog:
        updates["catalog"] = normalize_catalog(metadata.catalog)

    if metadata.integrations:
        updates["integration_types"] = \
            [*(metadata.integration_types or []), *metadata.integrations]
        updates["integrations"] = None


    return replace(metadata, **updates)


def getIntegrationLogger():
    return logging.getLogger('integration')
