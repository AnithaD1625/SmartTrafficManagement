import pandas as pd
from models import Light, Crossing

# Fuzzy Rules for Traffic Density:
# 1. If (Speed is Slow) and (Acceleration is Low) then (Traffic is Medium)
# 2. If (Speed is Slow) and (Acceleration is Medium) then (Traffic is Medium)
# 3. If (Speed is Slow) and (Acceleration is High) then (Traffic is High)
# 4. If (Speed is Medium) and (Acceleration is Low) then (Traffic is Low)
# 5. If (Speed is Medium) and (Acceleration is Medium) then (Traffic is Low)
# 6. If (Speed is Medium) and (Acceleration is High) then (Traffic is Medium)
# 7. If (Speed is Fast) and (Acceleration is Low) then (Traffic is Free)
# 8. If (Speed is Fast) and (Acceleration is Medium) then (Traffic is Free)
# 9. If (Speed is Fast) and (Acceleration is High) then (Traffic is Low)

def derive_context(df):
    """
    Derive context from traffic data using fuzzy rules
    """
    Entities = []
    density = "FREE"
    light_color = "RED"
    accident = "NO"

    for index, row in df.iterrows():
        # Determine light color
        if row["Current_Light_Status"] == "L1":
            light_color = "RED"
        elif row["Current_Light_Status"] == "L2":
            light_color = "YELLOW"
        elif row["Current_Light_Status"] == "L3":
            light_color = "GREEN"
        
        lightItem = Light(light_color, row["Current_Timer"])
        
        # Apply fuzzy rules to determine traffic density
        if row["Average_Speed"] <= 20.0 and row["Average_Acceleration"] <= 10.0:
            avg_speed = "LOW"
            avg_acc = "LOW"
            density = "MEDIUM"
        elif row["Average_Speed"] <= 20.0 and row["Average_Acceleration"] >= 10.0 and row["Average_Acceleration"] <= 35.0:
            avg_speed = "LOW"
            avg_acc = "MEDIUM"
            density = "MEDIUM"  
        elif row["Average_Speed"] <= 20.0 and row["Average_Acceleration"] > 35.0:
            avg_speed = "LOW"
            avg_acc = "HIGH"
            density = "HIGH"
        elif row["Average_Speed"] >= 20.0 and row["Average_Speed"] <= 50.0 and row["Average_Acceleration"] <= 10.0:
            avg_speed = "MEDIUM"
            avg_acc = "LOW"
            density = "LOW"
        elif row["Average_Speed"] >= 20.0 and row["Average_Speed"] <= 50.0 and row["Average_Acceleration"] >= 10.0 and row["Average_Acceleration"] <= 35.0:
            avg_speed = "MEDIUM"
            avg_acc = "MEDIUM"
            density = "LOW" 
        elif row["Average_Speed"] >= 20.0 and row["Average_Speed"] <= 50.0 and row["Average_Acceleration"] > 35.0:
            avg_speed = "MEDIUM"
            avg_acc = "HIGH"
            density = "MEDIUM"
        elif row["Average_Speed"] > 50.0 and row["Average_Acceleration"] <= 10.0:
            avg_speed = "HIGH"
            avg_acc = "LOW"
            density = "FREE"
        elif row["Average_Speed"] > 50.0 and row["Average_Acceleration"] >= 10.0 and row["Average_Acceleration"] <= 35.0:
            avg_speed = "HIGH"
            avg_acc = "MEDIUM"
            density = "FREE"
        elif row["Average_Speed"] > 50.0 and row["Average_Acceleration"] > 35.0:
            avg_speed = "HIGH"
            avg_acc = "HIGH"
            density = "LOW"
        else:
            density = "Error!"
        
        # Determine accident status
        if row["Automatic Incident Detection (AID)"] == 0:
            accident = "NO"
        else:
            accident = "YES"

        # Create crossing item
        crossingItem = Crossing(
            row["Crossing_Id"], 
            row["Lane_Id"], 
            row["Time"], 
            row["Average_Speed"], 
            row["Average_Acceleration"], 
            avg_speed, 
            avg_acc, 
            density, 
            accident
        )
        
        Entities.append({
            "Light": lightItem,
            "Crossing": crossingItem
        })
    
    return Entities


def handle_accidents(entities):
    """
    Process accident scenarios and determine appropriate traffic light responses
    """
    accident_scenarios = []
    
    for entity in entities:
        if entity["Crossing"].accident == "YES" and entity["Light"].light_color == "GREEN":
            scenario = {
                "crossing_id": entity["Crossing"].crossingID,
                "lane_id": entity["Crossing"].laneID,
                "time": entity["Crossing"].time,
                "timer": entity["Light"].timer,
                "light_status": entity["Light"].light_color,
                "action": "Change to blinking yellow",
                "duration": 60 - entity["Light"].timer,
                "message": f"Accident detected at {entity['Crossing'].crossingID}, {entity['Crossing'].laneID}. Changing to blinking yellow for {60 - entity['Light'].timer} seconds."
            }
            accident_scenarios.append(scenario)
        elif entity["Crossing"].accident == "YES" and entity["Light"].light_color == "RED":
            scenario = {
                "crossing_id": entity["Crossing"].crossingID,
                "lane_id": entity["Crossing"].laneID,
                "time": entity["Crossing"].time,
                "timer": entity["Light"].timer,
                "light_status": entity["Light"].light_color,
                "action": "Maintain RED then change to blinking yellow",
                "duration": 60,
                "message": f"Accident detected at {entity['Crossing'].crossingID}, {entity['Crossing'].laneID}. Maintaining RED for 60 seconds, then changing to blinking yellow."
            }
            accident_scenarios.append(scenario)
    
    return accident_scenarios


def optimize_traffic_flow(entities):
    """
    Optimize traffic flow based on traffic density and light status
    """
    # Identify lanes with low density but green light
    green_lanes_low_density = []
    # Identify lanes with high density but red light
    red_lanes_high_density = []
    
    for entity in entities:
        if entity["Light"].light_color == "GREEN" and (entity["Crossing"].density == "LOW" or entity["Crossing"].density == "FREE"):
            green_lanes_low_density.append({
                "crossing_id": entity["Crossing"].crossingID,
                "lane_id": entity["Crossing"].laneID,
                "density": entity["Crossing"].density,
                "time": entity["Crossing"].time,
                "light_color": entity["Light"].light_color
            })
        elif entity["Light"].light_color == "RED" and entity["Crossing"].density == "HIGH":
            red_lanes_high_density.append({
                "crossing_id": entity["Crossing"].crossingID,
                "lane_id": entity["Crossing"].laneID,
                "density": entity["Crossing"].density,
                "time": entity["Crossing"].time,
                "light_color": entity["Light"].light_color
            })
    
    # Identify potential light changes to optimize flow
    optimization_actions = []
    
    for green_lane in green_lanes_low_density:
        for red_lane in red_lanes_high_density:
            if green_lane["crossing_id"] == red_lane["crossing_id"]:
                action = {
                    "crossing_id": green_lane["crossing_id"],
                    "from_lane": green_lane["lane_id"],
                    "to_lane": red_lane["lane_id"],
                    "action": f"Switch GREEN from {green_lane['lane_id']} (density: {green_lane['density']}) to {red_lane['lane_id']} (density: {red_lane['density']})",
                    "time": green_lane["time"]
                }
                optimization_actions.append(action)
    
    return optimization_actions


if __name__ == "__main__":
    # This code runs when the script is executed directly
    df = pd.read_csv("traffic1.csv")
    entities = derive_context(df)
    
    # Print some sample entities
    for i, entity in enumerate(entities[:5]):
        print(f"\nEntity {i+1}:")
        print(f"Crossing ID: {entity['Crossing'].crossingID}")
        print(f"Lane ID: {entity['Crossing'].laneID}")
        print(f"Time: {entity['Crossing'].time}")
        print(f"Speed: {entity['Crossing'].textSpeed}")
        print(f"Acceleration: {entity['Crossing'].textAcc}")
        print(f"Traffic Density: {entity['Crossing'].density}")
        print(f"Light Status: {entity['Light'].light_color}")
        print(f"Timer: {entity['Light'].timer}")
        print(f"Accident: {entity['Crossing'].accident}")
    
    # Process accident scenarios
    accident_scenarios = handle_accidents(entities)
    print(f"\nFound {len(accident_scenarios)} accident scenarios")
    
    # Optimize traffic flow
    optimization_actions = optimize_traffic_flow(entities)
    print(f"\nFound {len(optimization_actions)} potential traffic flow optimizations")