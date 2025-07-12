from data_processor import DataProcessor
import os
dp = DataProcessor()  # Adjust path if needed
country_list = dp.get_countries()

print(len(country_list))
# # Save to text file so you can upload it here
# with open("cleaned_countries.txt", "w") as f:
#     for country in country_list:
#         f.write(f"{country}\n")