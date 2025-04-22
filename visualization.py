import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_traffic_density_distribution(entities):
    """
    Plot the distribution of traffic density across different lanes
    """
    # Extract density data from entities
    densities = [entity['Crossing'].density for entity in entities]
    
    # Count occurrences of each density category
    density_counts = {}
    for density in densities:
        if density in density_counts:
            density_counts[density] += 1
        else:
            density_counts[density] = 1
    
    # Create bar plot
    plt.figure(figsize=(10, 6))
    plt.bar(density_counts.keys(), density_counts.values(), color=['green', 'yellow', 'orange', 'red'])
    plt.title('Traffic Density Distribution')
    plt.xlabel('Density Category')
    plt.ylabel('Number of Occurrences')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('traffic_density_distribution.png')
    plt.close()

def plot_accident_locations(entities):
    """
    Plot the locations where accidents have occurred
    """
    # Extract accident data
    accident_data = []
    for entity in entities:
        if entity['Crossing'].accident == "YES":
            accident_data.append({
                'crossing_id': entity['Crossing'].crossingID,
                'lane_id': entity['Crossing'].laneID,
                'time': entity['Crossing'].time
            })
    
    if not accident_data:
        print("No accidents found in the data.")
        return
    
    # Create a figure showing accident locations
    plt.figure(figsize=(12, 8))
    
    # Group by crossing_id
    crossings = {}
    for accident in accident_data:
        if accident['crossing_id'] in crossings:
            crossings[accident['crossing_id']].append(accident['lane_id'])
        else:
            crossings[accident['crossing_id']] = [accident['lane_id']]
    
    # Plot as a heatmap-like visualization
    data = []
    for crossing, lanes in crossings.items():
        for lane in lanes:
            data.append([crossing, lane, lanes.count(lane)])
    
    df = pd.DataFrame(data, columns=['Crossing', 'Lane', 'Accidents'])
    pivot_table = df.pivot_table(index='Crossing', columns='Lane', values='Accidents', aggfunc='sum', fill_value=0)
    
    sns.heatmap(pivot_table, annot=True, cmap='YlOrRd', fmt='g')
    plt.title('Accident Locations by Crossing and Lane')
    plt.tight_layout()
    plt.savefig('accident_locations.png')
    plt.close()

def plot_speed_vs_acceleration(df):
    """
    Plot the relationship between average speed and average acceleration
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Average_Speed'], df['Average_Acceleration'], 
                c=df['Automatic Incident Detection (AID)'], cmap='coolwarm', alpha=0.7)
    plt.colorbar(label='Accident (1=Yes, 0=No)')
    plt.title('Average Speed vs. Average Acceleration')
    plt.xlabel('Average Speed')
    plt.ylabel('Average Acceleration')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('speed_vs_acceleration.png')
    plt.close()

def plot_traffic_by_crossing(entities):
    """
    Plot traffic density by crossing
    """
    # Prepare data
    data = []
    for entity in entities:
        data.append({
            'crossing_id': entity['Crossing'].crossingID,
            'density': entity['Crossing'].density
        })
    
    df = pd.DataFrame(data)
    
    # Count density categories by crossing
    crossing_density = df.groupby(['crossing_id', 'density']).size().unstack(fill_value=0)
    
    # Plot
    crossing_density.plot(kind='bar', stacked=True, figsize=(12, 8), 
                         colormap='viridis')
    plt.title('Traffic Density Distribution by Crossing')
    plt.xlabel('Crossing ID')
    plt.ylabel('Count')
    plt.legend(title='Density')
    plt.tight_layout()
    plt.savefig('traffic_by_crossing.png')
    plt.close()

def visualize_traffic_data(df, entities):
    """
    Generate all visualizations for the traffic data
    """
    print("Generating traffic density distribution plot...")
    plot_traffic_density_distribution(entities)
    
    print("Generating accident locations plot...")
    plot_accident_locations(entities)
    
    print("Generating speed vs. acceleration plot...")
    plot_speed_vs_acceleration(df)
    
    print("Generating traffic by crossing plot...")
    plot_traffic_by_crossing(entities)
    
    print("All visualizations have been generated.")

if __name__ == "__main__":
    # This code runs when the script is executed directly
    from context_derivation import derive_context
    
    # Load data
    df = pd.read_csv("traffic1.csv")
    
    # Derive context
    entities = derive_context(df)
    
    # Generate visualizations
    visualize_traffic_data(df, entities)