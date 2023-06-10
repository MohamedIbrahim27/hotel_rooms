# import pycountry

# # Retrieve the country code for Egypt
# country_code = 'EG'

# # Get the subdivision information for Egypt
# subdivisions = pycountry.subdivisions.get(country_code=country_code)

# # Filter and retrieve the governorates
# governorates = [subdivision.name for subdivision in subdivisions if subdivision.type == 'Governorate']

# # Print the governorates
# count = len(governorates)
# print("Number of governorates in Egypt:", count)

# for governorate in governorates:
#     print(governorate)
    
    
    
    
# # import pycountry

# # # Retrieve the country code for the United States
# # country_code = 'US'

# # # Get the subdivisions (states) for the United States
# # subdivisions = pycountry.subdivisions.get(country_code=country_code)

# # # Filter and retrieve the state names
# # states = [subdivision.name for subdivision in subdivisions if subdivision.type == 'State']

# # # Print the states
# # count = len(states)
# # print("Number of states in the United States:", count)

# # for state in states:
# #     print(state)

import pycountry

# Retrieve the country code for Saudi Arabia
country_code = 'SA'

# Get the subdivision information for Saudi Arabia
subdivisions = pycountry.subdivisions.get(country_code=country_code)

# Filter and retrieve the governorates
governorates = [subdivision.name for subdivision in subdivisions if subdivision.type == 'Governorate']

# Print the governorates
count = len(governorates)
print("Number of governorates in Saudi Arabia:", count)

for governorate in governorates:
    print(governorate)


