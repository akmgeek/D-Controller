from dronekit import connect, VehicleMode

def connect_to_vehicle(connection_string):
    """
    Connects to a drone using DroneKit and returns the vehicle object.

    Parameters:
        connection_string (str): The connection string for the drone, e.g. "udp:127.0.0.1:14550".

    Returns:
        vehicle (Vehicle): The connected drone vehicle object.
    """

    # Connect to the vehicle
    vehicle = connect(connection_string)

    # Wait for the vehicle to be ready
    vehicle.wait_ready('autopilot_version')

    # Print some vehicle info
    print('Vehicle connected:')
    print('  Mode: %s' % vehicle.mode.name)
    print('  GPS: %s' % vehicle.gps_0)
    print('  Battery: %s' % vehicle.battery)

    vehicle.mode = VehicleMode("TAKEOFF")

    return vehicle

# v =connect_to_vehicle("tcp:127.0.0.1:14550")
# v.mode