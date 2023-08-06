import numpy as np


def get_indexmatrix(shape, flatten=False):
    r"""Matrix of indices with $a_{ijk\dots} = [i,j,k,\dots] $ for shape (N, M, ..., len(shape))
    with the indices being listed in the last dimension.

    Note: Numpy indexing does not work this way but as indices per dimension.

    Args:
        shape (list, int): List of target shape, e.g. (2, 2).
        flatten (bool): Whether to flatten the output or keep input-shape. Default is False.

    Returns:
        np.array: Index array of shape (N, M, ..., len(shape)) e.g. [[[0,0],[0,1]],[[1,0],[1,1]]]
    """
    indarr = np.indices(shape)
    re_order = np.append(np.arange(1, len(shape) + 1), 0)
    indarr = indarr.transpose(re_order)
    if flatten:
        indarr = np.reshape(indarr, (np.prod(shape), len(shape)))
    return indarr


def coordinates_to_distancematrix(coord3d):
    """Transform coordinates to distance matrix. Will apply transformation on last dimension.
    Changing of shape (..., N, 3) -> (..., N, N).
    
    Arg:
        coord3d (np.array): Coordinates of shape (..., N, 3) for cartesian coordinates (x, y, z)
            and N the number of atoms or points. Coordinates are last dimension.

    Returns:
        np.array: distance matrix as numpy array with shape (..., N, N) where N is the number of atoms.
    """
    shape_3d = len(coord3d.shape)
    a = np.expand_dims(coord3d, axis=shape_3d - 2)
    b = np.expand_dims(coord3d, axis=shape_3d - 1)
    c = b - a
    d = np.sqrt(np.sum(np.square(c), axis=shape_3d))
    return d


def invert_distance(d, nan=0, posinf=0, neginf=0):
    """Invert distance array, e.g. distance matrix. Inversion is done for all entries.
    Keeps of shape of distance array (..., ) -> (..., ).
    
    Args:
        d (numpy array): Array of distance values of shape (..., )
        nan (value): Replacement for np.nan after division. Default is 0.
        posinf (value): Replacement for np.inf after division. Default is 0.
        neginf (value): Replacement for -np.inf after division. Default is 0.
        
    Returns:
        np.array: Inverted distance array as np.array of identical shape (..., ) and
            replaces np.nan and np.inf with e.g. 0
    """
    with np.errstate(divide='ignore', invalid='ignore'):
        c = np.true_divide(1, d)
        # c[c == np.inf] = 0
        c = np.nan_to_num(c, nan=nan, posinf=posinf, neginf=neginf)
    return c


def distance_to_gaussdistance(distance, gbins=20, grange=4, gsigma=0.4):
    """Convert distance array to smooth one-hot representation using Gaussian functions.
    Changes shape for gaussian distance (..., ) -> (..., gbins).
    The Default values match realistic units in Angstroem.
    
    Args:
        distance (numpy array): Array of distances of shape (..., )
        gbins (int): Number of Bins to sample distance from. Default is 20
        grange (value): Maximum distance to be captured by bins. Default is 4.0
        gsigma (value): Sigma of the gaussian function, determining the width/sharpness. Default is 0.4
    
    Returns:
        np.array: Array of gaussian distance with expanded last axis (..., gbins)
    """
    gamma = 1 / gsigma / gsigma * (-1) / 2
    d_shape = distance.shape
    edge_dist_grid = np.expand_dims(distance, axis=-1)
    edge_gaus_bin = np.arange(0, gbins, 1) / gbins * grange
    edge_gaus_bin = np.broadcast_to(edge_gaus_bin, np.append(np.ones(len(d_shape), dtype=np.int32),
                                                             edge_gaus_bin.shape))  # shape (1,1,...,GBins)
    edge_gaus_bin = np.square(edge_dist_grid - edge_gaus_bin) * gamma  # (N,M,...,1) - (1,1,...,GBins)
    edge_gaus_bin = np.exp(edge_gaus_bin)
    return edge_gaus_bin


def get_connectivity_from_inversedistancematrix(invdistmat, protons, radii_dict=None, k1=16.0, k2=4.0 / 3.0,
                                                cutoff=0.85, force_bonds=True):
    """Get connectivity table from inverse distance matrix defined at last dimensions (..., N, N) and
    corresponding bond-radii. Keeps shape with (..., N, N).
    Covalent radii, from Pyykko and Atsumi, Chem. Eur. J. 15, 2009, 188-197. 
    Values for metals decreased by 10% according to Robert Paton's Sterimol implementation. 
    Partially based on code from Robert Paton's Sterimol script, which based this part on Grimme's D3 code.
    
    Args:
        invdistmat (numpy array): Inverse distance matrix defined at last dimensions (..., N, N)
            distances must be in Angstroem not in Bohr
        protons (numpy array): An array of atomic numbers matching the invdistmat (..., N),
            for which the radii are to be computed.
        radii_dict (numpy array): Covalent radii for each element. If default=None, stored values are used.
            Otherwise array with covalent bonding radii. Example: np.array([0, 0.34, 0.46, 1.2, ...]) from
            {'H': 0.34, 'He': 0.46, 'Li': 1.2, ...}.
        k1 (value): K1-value. Defaults to 16
        k2 (value): K2-value. Defaults to 4.0/3.0
        cutoff (value): Cutoff value to set values to Zero (no bond). Defaults to 0.85
        force_bonds (value): Whether to force at least one bond in the bond table per atom (default = True).
        
    Returns:
        np.array: Connectivity table with 1 for chemical bond and zero otherwise of shape (..., N, N) -> (..., N, N)
    """
    # Dictionary of bond radii
    proton_raddi_dict = np.array(
        [0, 0.34, 0.46, 1.2, 0.94, 0.77, 0.75, 0.71, 0.63, 0.64, 0.67, 1.4, 1.25, 1.13, 1.04, 1.1, 1.02, 0.99, 0.96,
         1.76, 1.54, 1.33, 1.22, 1.21, 1.1, 1.07, 1.04, 1.0, 0.99, 1.01, 1.09, 1.12, 1.09, 1.15, 1.1, 1.14, 1.17, 1.89,
         1.67, 1.47, 1.39, 1.32, 1.24, 1.15, 1.13, 1.13, 1.19, 1.15, 1.23, 1.28, 1.26, 1.26, 1.23, 1.32, 1.31, 2.09,
         1.76, 1.62, 1.47, 1.58, 1.57, 1.56, 1.55, 1.51, 1.52, 1.51, 1.5, 1.49, 1.49, 1.48, 1.53, 1.46, 1.37, 1.31,
         1.23, 1.18, 1.16, 1.11, 1.12, 1.13, 1.32, 1.3, 1.3, 1.36, 1.31, 1.38, 1.42, 2.01, 1.81, 1.67, 1.58, 1.52, 1.53,
         1.54, 1.55])
    if radii_dict is None:
        radii_dict = proton_raddi_dict  # index matches atom number
    # Get Radii
    protons = np.array(protons, dtype=np.int)
    radii = radii_dict[protons]
    # Calculate
    shape_rad = radii.shape
    r1 = np.expand_dims(radii, axis=len(shape_rad) - 1)
    r2 = np.expand_dims(radii, axis=len(shape_rad))
    rmat = r1 + r2
    rmat = k2 * rmat
    rr = rmat * invdistmat
    damp = (1.0 + np.exp(-k1 * (rr - 1.0)))
    damp = 1.0 / damp
    if force_bonds:  # Have at least one bond
        maxvals = np.expand_dims(np.argmax(damp, axis=-1), axis=-1)
        np.put_along_axis(damp, maxvals, 1, axis=-1)
        # To make it symmetric transpose last two axis
        damp = np.swapaxes(damp, -2, -1)
        np.put_along_axis(damp, maxvals, 1, axis=-1)
        damp = np.swapaxes(damp, -2, -1)
    damp[damp < cutoff] = 0
    bond_tab = np.round(damp)
    return bond_tab


def define_adjacency_from_distance(distance_matrix, max_distance=np.inf, max_neighbours=np.inf, exclusive=True,
                                   self_loops=False):
    """Construct adjacency matrix from a distance matrix by distance and number of neighbours. Works for batches.
    
    This does not take into account special bonds (e.g. chemical) just a general distance measure.
    Tries to connect nearest neighbours.

    Args:
        distance_matrix (np.array): Distance Matrix of shape (..., N, N)
        max_distance (float, optional): Maximum distance to allow connections, can also be None. Defaults to np.inf.
        max_neighbours (int, optional): Maximum number of neighbours, can also be None. Defaults to np.inf.
        exclusive (bool, optional): Whether both max distance and Neighbours must be fulfilled. Defaults to True.
        self_loops (bool, optional): Allow self-loops on diagonal. Defaults to False.

    Returns:
        tuple: graph_adjacency, graph_indices
        
        - graph_adjacency (np.array): Adjacency Matrix of shape (..., N, N) of dtype=np.bool.
        - graph_indices (np.array): Flatten indices from former array that have adjacency == True.
    """
    distance_matrix = np.array(distance_matrix)
    num_atoms = distance_matrix.shape[-1]
    if exclusive:
        graph_adjacency = np.ones_like(distance_matrix, dtype=np.bool)
    else:
        graph_adjacency = np.zeros_like(distance_matrix, dtype=np.bool)
    inddiag = np.arange(num_atoms)
    # Make Indix Matrix
    indarr = np.indices(distance_matrix.shape)
    re_order = np.append(np.arange(1, len(distance_matrix.shape) + 1), 0)
    graph_indices = indarr.transpose(re_order)
    # print(graph_indices.shape)
    # Add Max Radius
    if max_distance is not None:
        temp = distance_matrix < max_distance
        # temp[...,inddiag,inddiag] = False
        if exclusive:
            graph_adjacency = np.logical_and(graph_adjacency, temp)
        else:
            graph_adjacency = np.logical_or(graph_adjacency, temp)
    # Add #Nieghbours
    if max_neighbours is not None:
        max_neighbours = min(max_neighbours, num_atoms)
        sorting_index = np.argsort(distance_matrix, axis=-1)
        # SortedDistance = np.take_along_axis(self.distance_matrix, sorting_index, axis=-1)
        ind_sorted_red = sorting_index[..., :max_neighbours + 1]
        temp = np.zeros_like(distance_matrix, dtype=np.bool)
        np.put_along_axis(temp, ind_sorted_red, True, axis=-1)
        if exclusive:
            graph_adjacency = np.logical_and(graph_adjacency, temp)
        else:
            graph_adjacency = np.logical_or(graph_adjacency, temp)
    # Allow self-loops
    if not self_loops:
        graph_adjacency[..., inddiag, inddiag] = False

    graph_indices = graph_indices[graph_adjacency]
    return graph_adjacency, graph_indices


def get_angle_indices(idx, is_sorted=False):
    """Compute index list for edge-pairs forming an angle.

    Args:
        idx (np.array): List of edge indices referring to nodes of shape (N, 2)
        is_sorted (bool): If edge indices are sorted, otherwise they will be sorted. Default is False.

    Returns:
        tuple: idx, idx_ijk, idx_ijk_ij

        - idx (np.array): Possibly sorted edge indices referring to nodes of shape (N, 2)
        - idx_ijk (np.array): Indices of nodes forming an angle as i<-j<-k of shape (M, 3)
        - idx_ijk_ij (np.array): Indices for an angle referring to edges of shape (M, 2)
    """

    if not is_sorted:
        order1 = np.argsort(idx[:, 1], axis=0, kind='mergesort')  # stable!
        ind1 = idx[order1]
        order2 = np.argsort(ind1[:, 0], axis=0, kind='mergesort')
        ind2 = ind1[order2]
        idx = ind2

    pair_label = np.arange(len(idx))
    idx_i = idx[:, 0]
    idx_j = idx[:, 1]
    uni_i, cnts_i = np.unique(idx_i, return_counts=True)
    reps = cnts_i[idx_j]
    idx_ijk_i = np.repeat(idx_i, reps)
    idx_ijk_j = np.repeat(idx_j, reps)
    idx_ijk_label_i = np.repeat(pair_label, reps)
    idx_j_tagged = np.concatenate([np.expand_dims(idx_j, axis=-1), np.expand_dims(pair_label, axis=-1)], axis=-1)
    idx_ijk_k_tagged = np.concatenate([idx_j_tagged[idx_i == x] for x in idx_j])  # This is not fully vectorized
    idx_ijk_k = idx_ijk_k_tagged[:, 0]
    idx_ijk_label_j = idx_ijk_k_tagged[:, 1]
    back_and_forth = idx_ijk_i != idx_ijk_k
    idx_ijk = np.concatenate([np.expand_dims(idx_ijk_i, axis=-1),
                              np.expand_dims(idx_ijk_j, axis=-1),
                              np.expand_dims(idx_ijk_k, axis=-1)], axis=-1)
    idx_ijk = idx_ijk[back_and_forth]
    idx_ijk_ij = np.concatenate([np.expand_dims(idx_ijk_label_i, axis=-1),
                                 np.expand_dims(idx_ijk_label_j, axis=-1)], axis=-1)
    idx_ijk_ij = idx_ijk_ij[back_and_forth]

    return idx, idx_ijk, idx_ijk_ij
