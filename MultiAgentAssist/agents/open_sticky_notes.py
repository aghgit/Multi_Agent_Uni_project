import subprocess


def open_sticky_notes_shell():
    # This launches Sticky Notes by its Package Family Name
    cmd = "start shell:AppsFolder\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe!App"
    try:
        subprocess.run(["cmd", "/c", cmd], check=True)
    except Exception as e:
        print(f"Shell launch failed: {e}")


open_sticky_notes_shell()
