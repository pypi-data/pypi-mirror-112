
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from .api.about_api import AboutApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from stackl_client.api.about_api import AboutApi
from stackl_client.api.functional_requirements_api import FunctionalRequirementsApi
from stackl_client.api.infrastructure_base_api import InfrastructureBaseApi
from stackl_client.api.outputs_api import OutputsApi
from stackl_client.api.policy_templates_api import PolicyTemplatesApi
from stackl_client.api.services_api import ServicesApi
from stackl_client.api.snapshots_api import SnapshotsApi
from stackl_client.api.stack_application_templates_api import StackApplicationTemplatesApi
from stackl_client.api.stack_infrastructure_templates_api import StackInfrastructureTemplatesApi
from stackl_client.api.stack_instances_api import StackInstancesApi
