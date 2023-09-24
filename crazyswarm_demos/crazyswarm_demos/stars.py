import matplotlib.pyplot as plt
import numpy as np

Hz = 20
a = 10
b = 7
def fx(t):
    # Parametric Equation defining x location at some time t
    # Note: if you need sin, cos, they are provided by numpy (np)
    # Just call np.sin(t) or np.cos(t)
    if t < 11*np.pi:
        return 0.07/4 * ((a-b) * np.cos(t) + b*np.cos((a/b - 1)*t)) # TODO
    else:
        return 0.07/4 * ((a+b) * np.cos(t) - b*np.cos((a/b + 1)*t))

def fy(t):
    # Parametric Equation defining y location at some time t
    return 0 # TODO

def fz(t):
    # Parametric Equation defining z location at some time t
    if t < 11*np.pi: 
        return 0.07/4 * (((a-b) * np.sin(t) - b*np.sin((a/b - 1)*t))-20) + 1.5 # TODO
    else:
        return 0.07/4 * (((a+b) * np.sin(t) - b*np.sin((a/b + 1)*t))-20) + 1.5
def get_velocity(waypoints):
    # Get velocity over time given a series of waypoints

    # Make an empty list that will hold values of velocity
    velocities = []

    # Loop through every waypoint
    for i, location in enumerate(waypoints):
        # For the first waypoint, initialize previous location
        if i == 0:
            prev_location = location

        # Append (add to list), the difference between current and previous location.
        # Multiply by Hz to correct for the size of timesteps
        velocities.append((location - prev_location) * Hz)

        prev_location = location
    
    return velocities
        

def get_acceleration(waypoints):
    # Get accelerations over time for a series of waypoints
    # (similar to how velocity is computed)
    velocities = get_velocity(waypoints)

    accelerations = []
    for i, velocity in enumerate(velocities):
        if i == 0:
            prev_velocity = velocity
        accelerations.append(velocity - prev_velocity)
        prev_velocity = velocity
    return accelerations

def make_graphs(timesteps, waypoints_x, waypoints_y, waypoints_z):
    # Get velocity and accelerations, make plots
    x_vel = get_velocity(waypoints_x)
    x_acc = get_acceleration(waypoints_x)

    y_vel = get_velocity(waypoints_y)
    y_acc = get_acceleration(waypoints_y)

    z_vel = get_velocity(waypoints_z)
    z_acc = get_acceleration(waypoints_z)

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)
    
    ax1.plot(timesteps, x_vel, label='Velocity')
    ax1.plot(timesteps, x_acc, label='Acceleration')
    ax1.set_title('X Velocity and Acceleration')
    ax1.legend()

    ax2.plot(timesteps, y_vel, label='Y Velocity')
    ax2.plot(timesteps, y_acc, label='Y Acceleration')
    ax2.set_title('Y Velocity and Acceleration')

    ax3.plot(timesteps, z_vel, label='Z Velocity')
    ax3.plot(timesteps, z_acc, label='Z Acceleration')
    ax3.set_title('Z Velocity and Acceleration')

    total_velocity = np.linalg.norm((x_vel, y_vel, z_vel), axis=0)
    total_acceleration = np.linalg.norm((x_acc, y_acc, z_acc), axis=0)
    ax4.plot(timesteps, total_velocity, label='Total Velocity')
    ax4.plot(timesteps, total_acceleration, label='Total Acceleration')
    ax4.set_title('Total Velocity and Acceleration')
    fig.tight_layout()
    plt.show(block=False)

    print("Maximum Velocity: ", np.max(total_velocity), "Maximum Acceleration: ", np.max(total_acceleration))
    print("Max X:", np.max(waypoints_x), "Min X:", np.min(waypoints_x))
    print("Max Y:", np.max(waypoints_y), "Min Y:", np.min(waypoints_y))
    print("Max Z:", np.max(waypoints_z), "Min Z:", np.min(waypoints_z))
    print("Total Time: ", timesteps[-1] - timesteps[0])

    ax = plt.figure().add_subplot(projection='3d')
    ax.plot(waypoints_x, waypoints_y, waypoints_z)
    plt.show()

def main():
    # Define the domain of the parametric function
    start_time = 0 # TODO
    end_time = 90 # TODO

    # Get evenly spaced timesteps between start_time and end_time
    timesteps = np.arange(start_time, end_time + 1/Hz, 1/Hz)

    # Initialize lists for waypoints
    waypoints_x = []
    waypoints_y = []
    waypoints_z = []

    # Loop through each timestep
    for t in timesteps:
        # Get desired positions at this timestep
        x = fx(t)
        y = fy(t)
        z = fz(t)

        waypoints_x.append(x)
        waypoints_y.append(y)
        waypoints_z.append(z)

    make_graphs(timesteps, waypoints_x, waypoints_y, waypoints_z)


if __name__ == '__main__':
    main()
