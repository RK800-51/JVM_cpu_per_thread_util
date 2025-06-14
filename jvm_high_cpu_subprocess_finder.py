import datetime
import os

from get_JVM_dumps import get_JVM_process_jps, dump_jstack
from get_top_snapshot import dump_top_snapshot
from parse_dumps import merge_top_jstack

def generate_report(threads: list, pid: int, output_dir: str = ".") -> str:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"cpu_usage_per_thread_jvm{pid}_{timestamp}.txt"
    filepath = os.path.join(output_dir, filename)

    print("=== Top JVM threads by 1 CPU core usage ===")
    for i, thread in enumerate(threads[:10], 1):
        print(f"{i}. nid: {thread['nid']} | CPU usage: {thread['cpu_usage']} % | name: {thread['name']}")

    try:
        with open(filepath, "w") as f:
            f.write("=== Full JVM Thread CPU per core Report ===\n")
            for thread in threads:
                f.write(f"[CPU%] {thread['cpu_usage']} [NID] {thread['nid']} [Thread name from jstack] {thread['name']}\n")
        print(f"Full report written to disk at {filepath}")
        return filepath
    except Exception as e:
        print(f"Failed to generate report due to: {e}")

def main():
    global processes

    # берем список процессов из jps JDK
    try:
        processes = get_JVM_process_jps()
    except RuntimeError as e:
        print(f"Error during getting processes list: {e}")

    # если подходящих процессов не найдено, то выходим из программы
    if not processes:
        print("No JVM processes found")
        return
    print("JVM applications running on this machine:")
    for pid, description in processes:
        print(f"{pid}: {description}")

    # создаем дампы jstack и top для каждого процесса JVM
    for pid, description in processes:
        try:
            print(f"Getting jstack dump for JVM process {pid}")
            jstack_filepath = dump_jstack(pid)
            print(f"Jstack dump for JVM process {pid}: {jstack_filepath}")
            top_filepath = dump_top_snapshot(pid)
            print(f"Top dump for JVM process {pid}: {top_filepath}")
        except Exception as e:
            print(f"Error during jstack run: {e}")

        # парсим дампы, получаем результирующий словарь с данными о потоках JVM, выводим отчет в терминал и в файл
        try:
            threads = merge_top_jstack(jstack_filepath, top_filepath)
            generate_report(threads, pid)
        except Exception as e:
            print(f"Error during jstack or top parsing: {e}")


if __name__ == "__main__":
    main()