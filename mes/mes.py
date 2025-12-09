import requests
import time
import random
from datetime import date, time as dt_time

BASE_URL = "http://127.0.0.1:5000/api/component_types"
HEADERS ={
        "Content-Type": "application/vnd.api+json"
    }

cur_id = 16000

def generate_component_type_data():
    global cur_id
    serv_life = random.randint(60, 300)
    quant = random.randint(0, 50)

    cur_id += 1

    return {
        "data": {
            "attributes": {
                "name": "",
                "manufacturer": "",
                "service_life": serv_life,
                "quantity":quant
            },
            "type": "ComponentType"
        }
    }

def measure_insert_time():

    data = generate_component_type_data()


    start = time.perf_counter()
    response = requests.post(BASE_URL, json=data, headers=HEADERS)
    end = time.perf_counter()

    if response.status_code != 201:
        print("Ошибка:", response.json())

    #measure_delete(20126 + year)

    return end - start


def measure_read(record_id):
    url = f"{BASE_URL}/{record_id}"
    start = time.perf_counter()
    response = requests.get(url, headers=HEADERS)
    end = time.perf_counter()
    if response.status_code != 200:
        print("READ Error:", response.json())
    return end - start

# --- UPDATE (PATCH) ---
def measure_update(record_id):
    url = f"{BASE_URL}/{record_id}"
    quant = random.randint(0, 50)
    data = {
            "data": {
                "attributes": {
                "quantity": quant
            },
            "type": "ComponentType",
            "id": str(record_id)
            }
    }
    start = time.perf_counter()
    response = requests.patch(url, json=data, headers=HEADERS)
    end = time.perf_counter()
    if response.status_code not in (200, 204):
        print("UPDATE Error:", response.json())
    return end - start

# --- DELETE ---
def measure_delete(record_id):
    url = f"{BASE_URL}/{record_id}"
    start = time.perf_counter()
    response = requests.delete(url, headers=HEADERS)
    end = time.perf_counter()
    if response.status_code not in (200, 204):
        print("DELETE Error:", response.json())
    return end - start

# for i in range(77802, 52802, -1):
#    measure_delete(i)
# #
# times = [measure_update(7527) for j in range(100)]
# avg_time = sum(times) / len(times)
# print(f"Среднее время через API: {avg_time * 1000:.3f} мс")

creates, reads, updates, deletes = [], [], [], []

# for i in range(15000):
#     measure_insert_time()

for i in range(500):
    creates.append(measure_insert_time())
    reads.append(measure_read(cur_id))
    updates.append(measure_update(cur_id))
    deletes.append(measure_delete(cur_id))

print(f"create: {(sum(creates) / len(creates)) * 1000:.3f}")
print(f"select: {(sum(reads) / len(reads)) * 1000:.3f}")
print(f"update: {(sum(updates) / len(updates)) * 1000:.3f}")
print(f"delete: {(sum(deletes) / len(deletes)) * 1000:.3f}")

print(cur_id)