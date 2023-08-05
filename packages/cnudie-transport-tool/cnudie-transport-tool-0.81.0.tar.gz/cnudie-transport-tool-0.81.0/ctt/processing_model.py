import dataclasses
import typing

import gci.componentmodel as cm


@dataclasses.dataclass
class ContainerImageUploadRequest:
    source_ref: str
    target_ref: str
    remove_files: typing.Sequence[str] = ()


@dataclasses.dataclass
class ProcessingJob:
    component: cm.Component
    resource: cm.Resource
    upload_request: ContainerImageUploadRequest
    processed_resource: cm.Resource = None  # added after re-upload
