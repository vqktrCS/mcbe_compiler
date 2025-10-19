import os
import json
import uuid
import argparse

def generate_uuid():
    return str(uuid.uuid4())

def create_manifest(folder, pack_name, pack_type, description, dependency_uuid=None):
    """Generate a valid Minecraft manifest.json for RP or BP."""
    os.makedirs(folder, exist_ok=True)

    header_uuid = generate_uuid()
    module_uuid = generate_uuid()

    manifest = {
        "format_version": 2,
        "header": {
            "description": f"{description} ({pack_type})",
            "name": f"{pack_name} {pack_type}",
            "uuid": header_uuid,
            "version": [1, 0, 0],
            "min_engine_version": [1, 21, 0]
        },
        "modules": [
            {
                "type": "resources" if pack_type == "RP" else "data",
                "uuid": module_uuid,
                "version": [1, 0, 0]
            }
        ]
    }

    # Add dependency if this is a Behavior Pack
    if pack_type == "BP" and dependency_uuid:
        manifest["dependencies"] = [{"uuid": dependency_uuid, "version": [1, 0, 0]}]

    file_path = os.path.join(folder, "manifest.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4)

    print(f"Created manifest.json for {pack_type}: {file_path}")
    return header_uuid


def main():
    parser = argparse.ArgumentParser(
        description="Generate a Minecraft Bedrock workspace with RP and BP folders."
    )
    parser.add_argument("--name", type=str, required=True, help="Base name of your addon")
    parser.add_argument("--desc", type=str, default="No description provided", help="Addon description")
    parser.add_argument("--path", type=str, default=".", help="Target directory for workspace")

    args = parser.parse_args()

    # Prepare workspace paths
    base_dir = os.path.abspath(args.path)
    rp_path = os.path.join(base_dir, "RP")
    bp_path = os.path.join(base_dir, "BP")

    print(f"\nGenerating workspace for '{args.name}'")
    print(f"Target directory: {base_dir}\n")

    # Create manifests and link BP dependency to RP
    rp_uuid = create_manifest(rp_path, args.name, "RP", args.desc)
    create_manifest(bp_path, args.name, "BP", args.desc, dependency_uuid=rp_uuid)

    print("\nWorkspace generation complete!")
    print(f"Created folders:\n - {rp_path}\n - {bp_path}")

if __name__ == "__main__":
    main()


