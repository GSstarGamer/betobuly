            exe_dir = get_original_exe_path()
            updater_path = os.path.join(exe_dir, "updater.py")

            subprocess.Popen(updater_path, creationflags=subprocess.CREATE_NO_WINDOW)