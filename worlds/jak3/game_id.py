import Utils

# this is the only thing. that's it :)
jak3_name = "Jak 3"

# Maximum base item ID, used for filler item offset calculations
# Current highest key item ID is 34, so we use a higher base for future expansion
jak3_max = 100000

# The executable name of the GOAL Kernel.
jak3_gk = "gk" + (".exe" if Utils.is_windows else "")

# The executable name of the GOAL Compiler.
jak3_goalc = "goalc" + (".exe" if Utils.is_windows else "")
