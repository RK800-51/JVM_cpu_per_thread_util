import datetime
import os
import subprocess


def dump_top_snapshot(pid: int, output_dir: str = ".") -> str | None:
    # возвращает путь к созданному дампу top <pid JVM>
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"top_snapshot_{pid}_{timestamp}.txt"
    filepath = os.path.join(output_dir, filename)

    try:
        with open(filepath, "w") as f:
            subprocess.run(["top", "-b", "-n", "1", "-Hp", str(pid)],
                           stdout=f, stderr=subprocess.STDOUT, check=True, text=True)
            return filepath
    except Exception as e:
        print(f"Error dumping top snapshot {pid}: {e}")
        return None
