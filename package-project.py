import os
import shutil
import zipfile

def package_source_project():
    workspace_root = os.path.abspath(os.getcwd())
    zip_filename = "website-project.zip"
    public_zip = os.path.join(workspace_root, "public", zip_filename)
    root_zip = os.path.join(workspace_root, zip_filename)
    dist_dir = os.path.join(workspace_root, "dist")
    dist_zip = os.path.join(dist_dir, zip_filename)

    # Directories to completely exclude from the source archive
    excluded_dirs = {
        'node_modules',
        '.git',
        '.cache',
        '.npm',
        '__pycache__',
        '.complete-project-staging',
        'export'
    }

    # Specific files to exclude (archives, logs, temp files)
    excluded_files = {
        'website-project.zip',
        'static-website.zip',
        '.DS_Store'
    }

    # Collect all actual project files
    files_to_pack = []

    for root, dirs, files in os.walk(workspace_root):
        # Filter directories in-place
        dirs[:] = [d for d in dirs if d not in excluded_dirs and not d.startswith('.')]
        
        for file in sorted(files):
            if file in excluded_files:
                continue
            if file.endswith('.tmp') or file.endswith('.log') or file.endswith('.zip'):
                continue
                
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, workspace_root)
            
            # Avoid packing any zip files that may reside in public/ or dist/
            if rel_path.endswith('.zip'):
                continue

            files_to_pack.append((full_path, rel_path))

    print(f"Total source project files to package: {len(files_to_pack)}")

    # Ensure public directory exists
    os.makedirs(os.path.join(workspace_root, "public"), exist_ok=True)

    # Write the zip archive directly at the archive root (no artificial nested parent folder)
    with zipfile.ZipFile(public_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        for full_path, rel_path in sorted(files_to_pack, key=lambda x: x[1]):
            zipf.write(full_path, rel_path)

    # Copy to workspace root and dist
    shutil.copy2(public_zip, root_zip)
    if os.path.exists(dist_dir):
        shutil.copy2(public_zip, dist_zip)

    size_mb = os.path.getsize(public_zip) / (1024 * 1024)
    print(f"Successfully generated {zip_filename} ({size_mb:.2f} MB, {len(files_to_pack)} files)")
    print(f"Saved at:\n - {public_zip}\n - {root_zip}")

if __name__ == '__main__':
    package_source_project()
