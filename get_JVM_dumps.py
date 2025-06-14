import datetime
import os
import subprocess


def get_JVM_process_jps():
    # ищем нужные java-процессы через JDK утилиту jps -l
    global result
    try:
        result = subprocess.run(["jps", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        processes = []
        for line in result.stdout.splitlines():
            if ("Main" in line) or ("Bootstrap" in line): # TODO: поменять на Bootstrap?
                pid, *description = line.strip().split(maxsplit=1)
                processes.append((int(pid), description[0] if description else "Unknown"))

        return processes
    except FileNotFoundError:
        raise RuntimeError("jps not found, please install JDK or make sure jps can be used, maybe user needs more permissions or Java directory is not added to PATH")
    except Exception as e:
        print(f"Error during jps run: {result.stderr}")
    return []

def dump_jstack(pid: int, output_dir: str = ".") -> str:
    # снимаем дамп потоков JVM-процессов, полученных из get_JVM_process_jps
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"jstack_{pid}_{timestamp}.txt"
    filepath = os.path.join(output_dir, filename)
    try:
        with open(filepath, "w") as f:
            subprocess.run(["jstack", str(pid)], stdout=f, stderr=subprocess.STDOUT, check=True)

        return filepath
    except FileNotFoundError:
        raise RuntimeError("jstack not found, please install JDK or make sure jps can be used")
    except Exception as e:
        raise RuntimeError(f"Error during jstack run: {e}")

