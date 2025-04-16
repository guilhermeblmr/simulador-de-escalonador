from dataclasses import dataclass, field
import heapq

def simulate_scheduler(tasks, cpu_count=4, slice_duration=5):
    """
    Simula escalonador com preempção ao fim de cada quantum.
    tasks: lista de dicts com chaves id, quantum, cpus_necessarias, duracao_total.
    Retorna uso de CPUs por fatia e tempo total.
    """
    @dataclass(order=True)
    class Task:
        priority: int
        id: str = field(compare=False)
        quantum: int = field(compare=False)
        cpus_needed: int = field(compare=False)
        remaining: int = field(compare=False)

    ready = []
    for t in tasks:
        heapq.heappush(
            ready,
            Task(
                priority=-t['quantum'],
                id=t['id'],
                quantum=t['quantum'],
                cpus_needed=t['cpus_necessarias'],
                remaining=t['duracao_total'],
            )
        )

    running = []
    cpu_free = list(range(cpu_count))
    use_logs = [[] for _ in range(cpu_count)]
    time = 0

    def record_interval(start, end, allocations):
        t = start
        while t < end:
            for cpu in range(cpu_count):
                assigned = '-'
                for _, task, cpus in allocations:
                    if cpu in cpus and task.remaining > 0:
                        assigned = task.id
                        break
                use_logs[cpu].append(assigned)
            t += slice_duration

    while ready or running:
        while ready and ready[0].cpus_needed <= len(cpu_free):
            task = heapq.heappop(ready)
            run_time = min(task.quantum, task.remaining)
            end_time = time + run_time
            cpus = [cpu_free.pop(0) for _ in range(task.cpus_needed)]
            running.append((end_time, task, cpus))

        if not running:
            record_interval(time, time + slice_duration, [])
            time += slice_duration
            continue

        next_end = min(r[0] for r in running)
        record_interval(time, next_end, running)
        time = next_end

        new_running = []
        for end_time, task, cpus in running:
            if end_time <= time:
                task.remaining -= min(task.quantum, task.remaining)
                for c in cpus:
                    cpu_free.append(c)
                if task.remaining > 0:
                    heapq.heappush(
                        ready,
                        Task(
                            priority=-task.quantum,
                            id=task.id,
                            quantum=task.quantum,
                            cpus_needed=task.cpus_needed,
                            remaining=task.remaining,
                        ),
                    )
            else:
                new_running.append((end_time, task, cpus))

        running = new_running
        cpu_free.sort()

    return use_logs, time


def print_table(logs, slice_duration=5):
    """
    Imprime de forma organizada uma tabela de uso de CPUs.
    """
    cpu_count = len(logs)
    num_slices = len(logs[0]) if cpu_count > 0 else 0
    header = ["Intervalo"] + [f"CPU{c}" for c in range(cpu_count)]
    rows = []
    for i in range(num_slices):
        start = i * slice_duration
        end = (i + 1) * slice_duration
        label = f"{start}-{end}s"
        row = [label] + [logs[c][i] for c in range(cpu_count)]
        rows.append(row)
    cols = list(zip(header, *rows))
    widths = [max(len(str(item)) for item in col) for col in cols]
    def fmt(items):
        return " | ".join(str(item).ljust(w) for item, w in zip(items, widths))
    sep = "-+-".join('-'*w for w in widths)
    print(fmt(header))
    print(sep)
    for row in rows:
        print(fmt(row))


if __name__ == '__main__':
    tasks = [
        {'id': 'T1', 'quantum': 20, 'cpus_necessarias': 2, 'duracao_total': 50},
        {'id': 'T2', 'quantum': 15, 'cpus_necessarias': 1, 'duracao_total': 30},
        {'id': 'T3', 'quantum': 10, 'cpus_necessarias': 1, 'duracao_total': 40},
        {'id': 'T4', 'quantum': 10, 'cpus_necessarias': 2, 'duracao_total': 60},
        {'id': 'T5', 'quantum': 15, 'cpus_necessarias': 4, 'duracao_total': 40},
        {'id': 'T6', 'quantum': 20, 'cpus_necessarias': 2, 'duracao_total': 30},
        {'id': 'T7', 'quantum': 15, 'cpus_necessarias': 2, 'duracao_total': 60},
        {'id': 'T8', 'quantum': 10, 'cpus_necessarias': 4, 'duracao_total': 30},
        {'id': 'T9', 'quantum': 20, 'cpus_necessarias': 4, 'duracao_total': 60},
        {'id': 'T10','quantum': 15, 'cpus_necessarias': 1, 'duracao_total': 20},
    ]
    slice_duration = 5
    logs, total = simulate_scheduler(tasks, cpu_count=4, slice_duration=slice_duration)
    print("Uso das CPUs: \n")
    print_table(logs, slice_duration=slice_duration)
    print(f"\nTempo total decorrido: {total} segundos")
