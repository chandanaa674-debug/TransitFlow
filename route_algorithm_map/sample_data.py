
# Bus data is now loaded from the actual bus-data.csv file.
# This keeps the same BUSES and STOPS imports used by
# route_algorithm.py and connection_algorithm.py.

from bus_data_loader import BUSES, STOPS

# Assumed waiting time when changing buses.
TRANSFER_WAIT_MINUTES = 5
