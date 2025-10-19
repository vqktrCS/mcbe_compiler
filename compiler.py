import os
import shutil
import ctypes
import threading
import time

# ===============================
# Get Minecraft Bedrock Directory
# ===============================
def get_minecraft_dir():
    local_appdata = os.environ.get("LOCALAPPDATA")
    if not local_appdata:
        return None
    base_path = os.path.join(local_appdata, "Packages")
    mc_package = "Microsoft.MinecraftUWP_8wekyb3d8bbwe"
    candidate = os.path.join(base_path, mc_package, "LocalState", "games", "com.mojang")
    if os.path.exists(candidate):
        return candidate
    for folder in os.listdir(base_path):
        if folder.startswith("Microsoft.MinecraftUWP"):
            alt = os.path.join(base_path, folder, "LocalState", "games", "com.mojang")
            if os.path.exists(alt):
                return alt
    return None


# ===============================
# Copying Logic
# ===============================
def copy_with_progress(src, dst, clear_dst=False):
    try:
        if clear_dst and os.path.exists(dst):
            shutil.rmtree(dst)
        os.makedirs(dst, exist_ok=True)

        for root, dirs, files in os.walk(src):
            rel_path = os.path.relpath(root, src)
            dest_dir = os.path.join(dst, rel_path)
            os.makedirs(dest_dir, exist_ok=True)
            for file in files:
                src_file = os.path.join(root, file)
                dest_file = os.path.join(dest_dir, file)
                shutil.copy2(src_file, dest_file)
                print(f"Copied: {src_file} → {dest_file}")
    except PermissionError as e:
        print(f"Permission denied: {e}")
    except Exception as e:
        print(f"Error copying {src} to {dst}: {e}")


# ===============================
# Message Box with Auto-Close
# ===============================
def show_timed_messagebox(title, message, duration=5):
    """
    Displays a Windows message box that auto-closes after `duration` seconds.
    """
    def close_box_after_delay():
        time.sleep(duration)
        # Find and close the message box by its title
        hwnd = ctypes.windll.user32.FindWindowW(None, title)
        if hwnd:
            ctypes.windll.user32.PostMessageW(hwnd, 0x0010, 0, 0)  # WM_CLOSE

    threading.Thread(target=close_box_after_delay, daemon=True).start()
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x40)  # 0x40 = MB_ICONINFORMATION


# ===============================
# Main Move Function
# ===============================
def move_dir(source_folder, game_folder, clear_dst=False):
    pack_types = [
        ("RP", "development_resource_packs"),
        ("BP", "development_behavior_packs"),
    ]
    moved_any = False

    for short, dev_folder in pack_types:
        src = os.path.join(source_folder, short)
        dst_root = os.path.join(game_folder, dev_folder)
        os.makedirs(dst_root, exist_ok=True)
        if os.path.exists(src):
            dst = os.path.join(dst_root, os.path.basename(src))
            print(f"Moving {short} from {src} to {dst}...")
            copy_with_progress(src, dst, clear_dst)
            moved_any = True
        else:
            print(f"{short} folder not found at {src}")

    if moved_any:
        print("Files moved. Type /reload all to launch world")
        show_timed_messagebox("vqktrCS's MCBE Compiler", "Files moved. Reload world (/reload all) to save changes (Closing in 5s)", 5)
    else:
        print("No RP or BP folders found in the source directory.")


# ===============================
# Main Entry
# ===============================
if __name__ == "__main__":
    print("Currently using vqktrCS's MCBE Compiler - Last Edited at 10/19/25")

    # Automatically use the current directory as source (repo root)
    default_source = os.getcwd()
    print(f"Default source folder: {default_source}")

    source = input(f"Enter source folder and click ENTER (default source: {default_source}): ").strip()
    if not source:
        source = default_source

    print(f"Copying Files from: {source}")

    game_folder = get_minecraft_dir()
    if not game_folder:
        print("Could not locate Minecraft Bedrock installation directory.")
        input("Press ENTER to exit...")
        exit(1)

    print(f"Moving to: {game_folder}")

    clear_prompt = input("Delete previous folders before copying? (Y/N): ").strip().lower()
    clear_dst = clear_prompt == "y"

    move_dir(source, game_folder, clear_dst)
