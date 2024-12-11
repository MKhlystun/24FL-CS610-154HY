There are four system configurations:

- **system_w_caches_v2.py**: A simulation system with cache hierarchy and a low locality workload.
- **system_w_caches_v2_sort.py**: A simulation system with cache hierarchy and a high locality workload.
- **system_wo_caches_v2.py**: A simulation system without cache hierarchy and a low locality workload.
- **system_wo_caches_v2_sort.py**: A simulation system without cache hierarchy and a high locality workload.

The **three_level.py** file contains the cache configuration, size, and policy.

The **stats.sh** and **st.sh** files are used to filter metrics from the statistics generated after simulations.

**arr_sort_random.cpp**: The code of a low locality workload.

**arr_sort_sort.cpp**: The code of a high locality workload.

