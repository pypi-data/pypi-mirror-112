import os

import spell.cli.utils  # for __file__ introspection
from spell.cli.utils.cluster_utils import kubectl

runs_namespace = "spell-runs"
runs_manifests_dir = os.path.join(
    os.path.dirname(spell.cli.utils.__file__), "kube_manifests", "spell-runs"
)

#########################
# Runs
#########################


# must be executed with elevated permissions (crd)
def add_argo():
    kubectl(
        "apply",
        "-f",
        os.path.join(runs_manifests_dir, "argo"),
        "-n",
        runs_namespace,
    )
