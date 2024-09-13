# Version 1 
# Constants
cost_grid_per_kWh = 0.15  # Cost of grid power per kWh
cost_diesel_per_kWh = 0.50  # Cost of diesel power per kWh
eta_charge = 0.9  # Battery charging efficiency
eta_discharge = 0.9  # Battery discharging efficiency
DOD = 0.2  # Depth of discharge
battery_capacity_Ah = 500  # Example battery capacity in Ah
rated_voltage = 48  # Rated voltage of battery in V

# Predicted power consumption (kW)
P_consumption = [5, 4.5, 3.8, 4.1, 3.6]  # Example predicted consumption over time

# Power source availability (kW)
P_solar = [2, 3, 4, 1, 0]  # Solar power available
P_grid = [5, 5, 5, 5, 5]  # Grid power available
P_diesel = 7  # Diesel generator capacity

# Initial battery SOC
SOC = 0.8  # 80% initial SOC

# Decision-making function
def calculate_power_usage(P_consumption, P_solar, P_grid, P_diesel, SOC):
    total_cost = 0
    battery_capacity_kWh = (battery_capacity_Ah * rated_voltage) / 1000  # Convert Ah to kWh
    battery_power_available = SOC * battery_capacity_kWh * eta_discharge  # kWh

    for i in range(len(P_consumption)):
        # Start with solar power
        P_remaining = P_consumption[i] - P_solar[i]
        P_solar_used = min(P_consumption[i], P_solar[i])

        # Use battery power next
        if P_remaining > 0 and battery_power_available > 0:
            P_battery_used = min(P_remaining, battery_power_available)
            P_remaining -= P_battery_used
            battery_power_available -= P_battery_used
            SOC = battery_power_available / (battery_capacity_kWh * eta_discharge)

        # Use grid power if available and needed
        if P_remaining > 0 and P_grid[i] > 0:
            P_grid_used = min(P_remaining, P_grid[i])
            P_remaining -= P_grid_used
            total_cost += P_grid_used * cost_grid_per_kWh

        # Use diesel power if everything else is insufficient
        if P_remaining > 0:
            P_diesel_used = min(P_remaining, P_diesel)
            total_cost += P_diesel_used * cost_diesel_per_kWh
            P_remaining -= P_diesel_used

        # Charge battery if excess solar power
        if P_solar[i] > P_consumption[i]:
            excess_solar = P_solar[i] - P_consumption[i]
            battery_charge_potential = min(excess_solar, (1 - SOC) * battery_capacity_kWh * eta_charge)
            SOC += battery_charge_potential / (battery_capacity_kWh * eta_charge)
            battery_power_available += battery_charge_potential

        # Output summary for each time step
        print(f"Hour {i+1}: Solar used: {P_solar_used} kW, "
              f"Battery used: {P_battery_used if 'P_battery_used' in locals() else 0} kW, "
              f"Grid used: {P_grid_used if 'P_grid_used' in locals() else 0} kW, "
              f"Diesel used: {P_diesel_used if 'P_diesel_used' in locals() else 0} kW, "
              f"SOC: {SOC:.2f}, Total Cost: {total_cost:.2f} USD")

    return total_cost

# Run the function
total_cost = calculate_power_usage(P_consumption, P_solar, P_grid, P_diesel, SOC)
print(f"\nTotal operation cost over time: {total_cost:.2f} USD")
