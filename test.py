# import multiprocessing
# import math

# def cpu_stress():
#     while True:
#         math.sqrt(12345)  # Some non-trivial operation

# if __name__ == "__main__":
#     num_processes = multiprocessing.cpu_count()
#     processes = []

#     for _ in range(num_processes):
#         p = multiprocessing.Process(target=cpu_stress)
#         p.start()
#         processes.append(p)

#     for p in processes:
#         p.join()


# # import time

# # def allocate_memory(mb):
# #     try:
# #         block = bytearray(mb * 1024 * 1024)  # Allocate MBs
# #         print(f"Allocated {mb} MB")
# #         time.sleep(60)  # Hold it for a minute
# #     except MemoryError:
# #         print("Failed to allocate. MemoryError!")

# # if __name__ == "__main__":
# #     allocate_memory(60000)  # Try to allocate 8 GB

print("hi")!