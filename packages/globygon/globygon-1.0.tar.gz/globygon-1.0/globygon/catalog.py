import numpy as np
""" 
Brian Jackson & Dida Markovic, 2021
"""

class Catalog:
    """
    A class to contain points in right ascension and declination (RA/Dec) and
    providing the functionality to calculate the center-of-mass of those points
    in RA/Dec

    Args:
        RA: the right ascension in radians as an array or float 
        Dec: the declination in radians as an array or float

    Written by Dida Markovic and Brian Jackson (bjackson@boisestate.edu) in
    2021 as part of the Code/Astro Workshop
    """

    def __init__(self, RA, Dec):
        
        self.RA = RA
        self.Dec = Dec

        self.x, self.y, self.z = None, None, None

        self.center_of_mass = None

    def _convert_RADec_to_Cartesian(self):
        """(Private) Converts right ascension (RA) and declination (Dec) into Cartesian 
        coordinates (x,y,z) assuming a radius = 1.
        
        The x-axis runs along a line of zero degrees Dec and RA, the y-axis
        along zero degrees Dec and 90 degrees RA, and the z-axis along 90
        degrees Dec.

        Args:
            None

        Returns:
            x: Cartesian x coordinate
            y: Cartesian y coordinate
            z: Cartesian z coordinate
        
        """
    
        self.x = np.cos(self.Dec)*np.cos(self.RA)
        self.y = np.cos(self.Dec)*np.sin(self.RA)
        self.z = np.sin(self.Dec)
    
        return self.x, self.y, self.z

    def _convert_Cartesian_to_RADec(self, x, y, z):
        """(Private) Converts Cartesian x, y, and z coordinates into right ascension (RA) and
        declination (Dec) as measured in radians

        The x-axis runs along a line of zero degrees Dec and RA, the y-axis
        along zero degrees Dec and 90 degrees RA, and the z-axis along 90
        degrees Dec.

        Args:
            x/y/z: floats or vectors of Cartesian coordinates

        Returns:
            list: the RA and Dec corresponding to the given x, y, and z
            coordinates
        """

        # Check that there are not any points with (x, y, z) = (0, 0, 0)
        if(isinstance(x, np.ndarray)):
            ind = np.argwhere((x == 0.) & (y == 0.) & (z == 0.))
            if(len(x[ind]) > 0):
                raise(ValueError("Cartesian coordinates are all zero!"))
        elif(isinstance(x, float)):
            if((x == 0.) & (y == 0.) & (z == 0.)):
                raise(ValueError("Cartesian coordinates are all zero!"))
        
        # Normalize back to unit sphere
        R = np.sqrt(x**2 + y**2 + z**2)
        
        Dec = np.arcsin(z/R)
        RA = np.arctan2(y/R,x/R)
        # Check to make sure RA is the right data type & make sure we return the angle in the right quadrant
        try:
            RA[RA<0]+=2.*np.pi
        except TypeError:
            if RA<0: RA+=2.*np.pi
            
        return RA, Dec

    def calculate_center_of_mass(self):
        """
        With a Catalog class instantiated and a list of RA/Dec values
        initialized, this method returns the RA/Dec of the center-of-mass for
        the RA/Dec points

        Args:
            None

        Returns: 
            list: RA/Dec of center-of-mass in radians
        """

        # Convert RA/Dec of the catalogue entries to Cartesian and save if not yet done
        if self.x is None or self.y is None or self.z is None:
            self._convert_RADec_to_Cartesian()

        # Calculate Cartesian center of mass
        mean_x, mean_y, mean_z = self.x.mean(), self.y.mean(), self.z.mean()
        self._com_Cart = mean_x, mean_y, mean_z

        # Convert to RA&Dec and project to sphere (simply by setting r=1)
        self.center_of_mass = self._convert_Cartesian_to_RADec(mean_x, mean_y, mean_z)
        return self.center_of_mass
    
    def calculate_dist_from_com(self,point=None):
        """ 
        With a Catalog class instantiated, a list of RA/Dec values
        initialized and a calculated centre of mass, this method returns the 
        distance of the center-of-mass to the RA/Dec points

        Args:
            point (tuple): arbitrary point (if different from the com) to calculate distance from
                           RA/Dec in radians expected

        Returns: 
            list: distances of the RA/Dec points to the center-of-mass in radians
        
        """

        # First catalogue to Cartesian if not already done
        if self.x is None or self.y is None or self.z is None:
            self._convert_RADec_to_Cartesian()

        if point is None:
            # Get the center of mass if the point is not given
            self.calculate_center_of_mass()
            point = self._com_Cart
        else:
            # Convert to Cartesian from radec
            point = [np.cos(point[1])*np.cos(point[0]),
                     np.cos(point[1])*np.sin(point[0]),
                     np.sin(point[1])]
 
        # Calculate Cartesian distances
        dx, dy, dz = self.x-point[0], self.y-point[1], self.z-point[2]
        dists = np.sqrt(dx**2 + dy**2 + dz**2)

        # Project to R=1 sphere
        R = 1
        return 2.*R*np.arcsin((0.5*dists/R))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="File name containing three columns with the last two containing RA/Dec values")
    args = parser.parse_args()

    filename = args.file
    data = np.genfromtxt(filename, comments='#', names=['ID', 'RA', 'Dec'], delimiter=' ')
    degtorad = np.pi/180.

    our_catalog = Catalog(data['RA']*degtorad, data['Dec']*degtorad)
    print(our_catalog.calculate_center_of_mass())
