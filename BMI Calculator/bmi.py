# Define a function to calculate BMI
def calculate_bmi(weight_kg, height_cm):
    # Convert height from centimeters to meters
    height_m = height_cm / 100

    # Calculate BMI using the formula: weight / (height in meters)^2
    bmi = weight_kg / (height_m ** 2)

    # Determine the BMI category based on the value
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 24.9:
        category = "Normal weight"
    elif 25 <= bmi < 29.9:
        category = "Overweight"
    else:
        category = "Obese"

    # Return the BMI value rounded to 2 decimal places, and the category
    return round(bmi, 2), category


# -------- Main program starts here --------

# Ask the user to enter their weight and height
weight = float(input("Enter your weight in kilograms (kg): "))
height = float(input("Enter your height in centimeters (cm): "))

# Call the function and store the results
bmi_result, bmi_category = calculate_bmi(weight, height)

# Print the results
print(f"\nYour BMI is: {bmi_result}")
print(f"Health Category: {bmi_category}")
