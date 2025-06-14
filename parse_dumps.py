import re


def parse_jstack(file_path: str) -> dict:
    # возвращает словарь {nid (int): thread_name (str)}
    threads = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if "nid" in line:
                name_match = re.search(r'"(.+?)"', line)
                nid_match = re.search(r'nid=(0x[\da-fA-F]+|\d+)', line)

                if name_match and nid_match:
                    name = name_match.group(1)
                    nid_raw = nid_match.group(1)

                    try:
                        nid = int(nid_raw, 16) if nid_raw.startswith("0x") else int(nid_raw)
                        threads[nid] = name
                    except ValueError:
                        continue

    return threads

def parse_top(file_path: str) -> dict:
    # возвращает словарь {nid (int): cpu_usage (float)}
    cpu_data = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) > 8 and parts[0].isdigit():
                try:
                    nid = int(parts[0])
                    cpu_usage = float(parts[8])
                    cpu_data[nid] = cpu_usage
                except ValueError:
                    continue

    return cpu_data

def merge_top_jstack(jstack_file: str, top_file: str) -> list:
    # мерджим полученный результат в список топ 10 потоков-потребителей CPU
    threads = parse_jstack(jstack_file)
    cpu_data = parse_top(top_file)
    result = []

    for nid in threads.keys():
        if nid in cpu_data:
            result.append({
                "nid": nid,
                "name": threads[nid],
                "cpu_usage": cpu_data[nid]
            })
    # сортировка по убыванию CPU
    result.sort(key=lambda x: x["cpu_usage"], reverse=True)
    return result

