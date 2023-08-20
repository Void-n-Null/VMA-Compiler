def compute_texture_axes(plane):
    # Define the default world axes
    world_axes = [
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1)
    ]
    
    # Find the primary axis (normal axis) of the plane
    primary_axis = max(world_axes, key=lambda ax: abs(dot_product(ax, plane)))

    # Uaxis is perpendicular to both the normal axis and the world up axis
    uaxis = cross_product(primary_axis, (0, 0, 1))
    
    # Vaxis is perpendicular to both the normal axis and the uaxis
    vaxis = cross_product(primary_axis, uaxis)

    return uaxis, vaxis

def cross_product(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0]
    )
    
def dot_product(a, b):
    return sum(a[i] * b[i] for i in range(3))