import matplotlib.pyplot as plt

# Данные
queries = [0, 1000, 5000, 15000, 25000, 50000, 75000, 100000]

insert_times = [14.990, 15.861, 17.087, 15.604, 16.861, 17.785, 16.194, 15.885]
select_times = [8.546, 9.136, 9.061, 9.159, 10.757, 10.329, 9.217, 8.933]
update_times = [15.231, 15.852, 16.258, 15.797, 17.812, 18.189, 16.339, 16.877]
delete_times = [10.694, 11.328, 11.450, 11.179, 13.003, 12.742, 11.505, 12.200]
# Построение графика
plt.figure(figsize=(10, 6))

plt.plot(queries, insert_times, marker='*', label='Insert')
plt.plot(queries, select_times, marker='s', label='Select')
plt.plot(queries, update_times, marker='.', label='Update')
plt.plot(queries, delete_times, marker='o', label='Delete')

plt.xscale('log')  # Логарифмическая шкала по X, т.к. запросов сильно разное количество
plt.xlabel('Количество записей')
plt.ylabel('Время выполнения (мс)')
#plt.title('Время выполнения операций с БД')
plt.legend()
plt.grid(True, which="both", ls="--", linewidth=0.5)

plt.savefig("graph.png")
plt.show()