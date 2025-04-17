## Simulação de Escalonamento de Tarefas

Este projeto implementa, em Python, uma simulação de escalonamento de tarefas em um sistema com múltiplas CPUs. São comparadas duas abordagens:

1. **FIFO com Prioridade por Quantum**: Tarefas com maior quantum têm prioridade. A preempção ocorre apenas ao final de cada quantum.
2. **EASY Backfilling**: Também prioriza o quantum, mas aproveita os momentos de ociosidade das CPUs para executar tarefas menores, desde que não atrasem a próxima tarefa prioritária.

---

### Estrutura do Código

- `simulate_scheduler(tasks, cpu_count=4, slice_duration=5)`:
  - Recebe uma lista de tarefas com as seguintes propriedades: `id`, `quantum`, `cpus_necessarias` e `duracao_total`.
  - Retorna um registro do uso das CPUs por fatia de tempo e o tempo total de execução.

- `simulate_scheduler_backfill(tasks, cpu_count=4, slice_duration=5)`:
  - Tem a mesma estrutura da função anterior, mas aplica a estratégia EASY Backfilling para melhorar a utilização dos núcleos disponíveis.

- `print_table(logs, slice_duration=5)`:
  - Formata e imprime os registros de uso das CPUs ao longo do tempo, de forma tabular.

- `compare_strategies(tasks)`:
  - Executa ambas as simulações, exibe as tabelas de uso e compara os tempos totais, indicando o ganho obtido pela estratégia com backfilling.

---

### Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/guilhermeblmr/simulador-de-escalonador.git
   ```

2. Certifique-se de que o Python 3.7 ou superior está instalado.

3. Execute o script principal:
   ```bash
   python index.py
   ```

4. A saída no terminal incluirá:

   - Tabela de uso das CPUs utilizando FIFO com prioridade por quantum.
   - Tempo total de execução dessa estratégia.
   - Tabela de uso das CPUs com a estratégia EASY Backfilling.
   - Tempo total de execução otimizado.
   - Diferença de tempo entre as abordagens.

---

### Exemplo de Saída

```
=== FIFO com Prioridade ===
Intervalo | CPU0 | CPU1 | CPU2 | CPU3
----------+------+------+------+-----
0-5s      | T1   | T1   | T5   | T5
5-10s     | T1   | T1   | T5   | T5
...       | ...  | ...  | ...  | ...

Tempo total: 200s

=== EASY Backfilling ===
Intervalo | CPU0 | CPU1 | CPU2 | CPU3
----------+------+------+------+-----
0-5s      | T1   | T1   | T9   | T9
5-10s     | T1   | T1   | T9   | T9
...       | ...  | ...  | ...  | ...

Tempo total: 180s

Melhoria de tempo: 20s
```

---

### Personalização

- **Número de CPUs**: Ajuste o parâmetro `cpu_count` para simular diferentes quantidades de núcleos.
- **Duração da Fatia de Tempo**: Modifique o `slice_duration` para alterar o tempo de cada fatia (valor padrão é 5 segundos).
- **Lista de Tarefas**: Altere os valores da lista `tasks` no bloco `if __name__ == '__main__':` para simular diferentes cenários.

---

### Possíveis Melhorias Futuras

- Adicionar gráficos (como diagramas de Gantt) para visualização do escalonamento.
- Incluir suporte para outras estratégias de escalonamento, como Round-Robin e Fair Share.
- Exportar os logs de execução para arquivos CSV ou Excel.

---

### Autores

- Guilherme Bloemer
- Eduardo Büsemayer
- Felipe Soares
- Felipe Serrano

