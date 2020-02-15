# resources for the simulation runner

SIMION_path = "\"C:\\Program Files (x86)\\SIMION-8.0\\simion.exe\""

fly2_base_string = """particles @
  coordinates = 0,
  standard_beam @
    n = {num},
    tob = 0,
    mass = 0.000548579903,
    charge = -1,
    ke = 1e-006,
    cwf = 1,
    color = 3,
    direction = vector(0, -1, 0),
    position = gaussian3d_distribution @
      mean = vector(10.65, 20.8, 10.65),
      stdev = vector(0.1895, 0.059, 0.1895)
    #
  #
#"""
