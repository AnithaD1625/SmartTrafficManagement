import pandas as pd
import matplotlib.pyplot as plt
from models import Light, Crossing
from context_derivation import derive_context, handle_accidents, optimize_traffic_flow
from visualization import visualize_traffic_data
from data_processing import process_data

def main():
    """
    Main function to run the Smart Traffic Management System
    """
    print("Smart Traffic Management System")
    print("-" * 30)
    
    # Load and process data
    print("\nLoading and processing traffic data...")
    df = pd.read_csv("traffic1.csv")
    process_data(df)
    
    # Derive context from data
    print("\nDeriving context from traffic data...")
    entities = derive_context(df)
    print(f"Processed {len(entities)} traffic scenarios")
    
    # Handle accident scenarios
    print("\nAnalyzing accident scenarios...")
    accident_scenarios = handle_accidents(entities)
    print(f"Found {len(accident_scenarios)} accident scenarios")
    
    if accident_scenarios:
        print("\nAccident Scenarios:")
        for i, scenario in enumerate(accident_scenarios):
            print(f"\nScenario {i+1}:")
            print(f"Location: Crossing {scenario['crossing_id']}, Lane {scenario['lane_id']}")
            print(f"Time: {scenario['time']}")
            print(f"Action: {scenario['action']}")
            print(f"Message: {scenario['message']}")
    
    # Optimize traffic flow
    print("\nAnalyzing traffic flow optimization opportunities...")
    optimization_actions = optimize_traffic_flow(entities)
    print(f"Found {len(optimization_actions)} potential traffic flow optimizations")
    
    if optimization_actions:
        print("\nTraffic Flow Optimization Actions:")
        for i, action in enumerate(optimization_actions[:5]):  # Show first 5 actions
            print(f"\nAction {i+1}:")
            print(f"Crossing: {action['crossing_id']}")
            print(f"Time: {action['time']}")
            print(f"Action: {action['action']}")
    
    # Generate visualizations
    print("\nGenerating traffic data visualizations...")
    visualize_traffic_data(df, entities)
    
    print("\nSmart Traffic Management System analysis complete.")


if __name__ == "__main__":
    main()