"""
Script for documenting the code of the LEffectModel component.
"""
import os
import base.documentation
import LEffectModel

root_folder = os.path.abspath(os.path.join(os.path.dirname(base.__file__), ".."))
base.documentation.document_component(
    LEffectModel.LEffectModel("LEffectModel", None, None),
    os.path.join(root_folder, "..", "variant", "LEffectModel", "README.md"),
    os.path.join(root_folder, "..", "variant", "mc.xml"),
    "IndEffect_StepsRiverNetwork_SD_Species1"
)
base.documentation.write_changelog(
    "LEffectModel component",
    LEffectModel.LEffectModel.VERSION,
    os.path.join(root_folder, "..", "variant", "LEffectModel", "CHANGELOG.md")
)
base.documentation.write_contribution_notes(
    os.path.join(root_folder, "..", "variant", "LEffectModel", "CONTRIBUTING.md"))
base.documentation.write_repository_info(
    os.path.join(root_folder, "..", "variant", "LEffectModel"),
    os.path.join(root_folder, "..", "variant", "LEffectModel", "repository.json"),
    os.path.join(root_folder, "..", "..", "..", "versions.json"),
    "component"
)
