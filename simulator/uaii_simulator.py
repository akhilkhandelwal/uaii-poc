import time
import random
from prometheus_client import start_http_server, Counter, Gauge

# --- METRIC DEFINITIONS ---
# 1. App Layer (Tokens)
TOKENS = Counter('uaii_tokens_total', 'Total AI tokens generated')
# 2. Hardware Layer (GPU & Power)
GPU_TEMP = Gauge('uaii_gpu_temp_c', 'GPU Junction Temperature (Celsius)')
GPU_POWER = Gauge('uaii_gpu_power_w', 'GPU Power Draw (Watts)')
COOLING_FLOW = Gauge('uaii_cooling_flow_percent', 'Liquid Cooling Flow Rate (%)')
# 3. Network Layer (Fabric)
TAIL_LATENCY = Gauge('uaii_fabric_latency_ms', 'InfiniBand Tail Latency (ms)')
SM_OCCUPANCY = Gauge('uaii_sm_occupancy_percent', 'GPU Streaming Multiprocessor Occupancy (%)')

def run_simulation():
    cycle_time = 0
    
    while True:
        # 60-second cycle: 0-20 (Normal), 20-40 (Thermal Event), 40-60 (Straggler Event)
        phase = cycle_time % 60 

        if phase < 20:
            # PHASE 1: NORMAL OPERATION
            COOLING_FLOW.set(100.0)
            GPU_TEMP.set(random.uniform(60, 65))
            GPU_POWER.set(random.uniform(300, 320))
            TAIL_LATENCY.set(random.uniform(1, 3))
            SM_OCCUPANCY.set(random.uniform(85, 95))
            TOKENS.inc(random.randint(150, 200)) # High Token throughput

        elif phase < 40:
            # PHASE 2: THERMAL ANOMALY (Innovation 1 Demo)
            # Cooling drops FIRST, then Temp rises 
            COOLING_FLOW.set(random.uniform(40, 50))
            # Temp spikes because cooling dropped
            GPU_TEMP.set(random.uniform(82, 88)) 
            GPU_POWER.set(random.uniform(350, 380))
            TAIL_LATENCY.set(random.uniform(1, 3))
            SM_OCCUPANCY.set(random.uniform(70, 80)) # Slight throttle
            TOKENS.inc(random.randint(100, 120)) # Reduced throughput

        else:
            # PHASE 3: NETWORK STRAGGLER (Innovation 2 Demo)
            COOLING_FLOW.set(100.0)
            GPU_TEMP.set(random.uniform(60, 65))
            GPU_POWER.set(random.uniform(300, 320))
            # Latency spikes -> GPUs wait for data -> SM Occupancy crashes
            TAIL_LATENCY.set(random.uniform(45, 60)) 
            SM_OCCUPANCY.set(random.uniform(15, 25)) 
            TOKENS.inc(random.randint(20, 40)) # Massive drop in Token generation

        cycle_time += 1
        time.sleep(1) # Emit metrics every 1 second

if __name__ == '__main__':
    start_http_server(8000)
    print("UAII Data Center Simulator is running on port 8000...")
    run_simulation()
