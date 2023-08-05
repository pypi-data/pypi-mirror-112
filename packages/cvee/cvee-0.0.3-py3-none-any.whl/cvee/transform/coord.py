import numpy as np
import torch


def create_grid(origin=None, size=None, resolution=None, return_tensor=False):
    """Create a 3D grid.

    Args:
        origin (list, optional): The (bottom, left, back) corner of the grid,
            note that it's not the center
        size (list, optional): The 3D size of the grid.
        resolution (list, optional): The resolution of the grid.
        return_tensor (bool, optional): Return `torch.tensor` or `np.array`.

    Returns:
        The points in the 3D grid.
    """

    if origin is None:
        origin = [-0.5, -0.5, -0.5]
    if size is None:
        size = [1.0, 1.0, 1.0]
    if resolution is None:
        resolution = [64, 64, 64]

    step_size = [size[i] / (resolution[i] - 1) for i in range(3)]

    if return_tensor:
        overall_index = torch.arange(0, resolution[0] * resolution[1] * resolution[2], dtype=torch.int64)
    else:
        overall_index = np.arange(0, resolution[0] * resolution[1] * resolution[2], dtype=np.int64)

    if return_tensor:
        points = torch.zeros(resolution[0] * resolution[1] * resolution[2], 3, dtype=torch.float)
    else:
        points = np.zeros((resolution[0] * resolution[1] * resolution[2], 3), dtype=np.float)

    # transform first 3 columns to be the x, y, z index
    points[:, 2] = overall_index % resolution[2]
    points[:, 1] = (overall_index // resolution[2]) % resolution[1]
    points[:, 0] = ((overall_index // resolution[2]) // resolution[1]) % resolution[0]

    # transform first 3 columns to be the x, y, z coordinate
    points[:, 0] = (points[:, 0] * step_size[0]) + origin[0]
    points[:, 1] = (points[:, 1] * step_size[1]) + origin[1]
    points[:, 2] = (points[:, 2] * step_size[2]) + origin[2]

    points = points.reshape((resolution[0], resolution[1], resolution[2], 3))

    return points
