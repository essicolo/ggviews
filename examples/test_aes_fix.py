"""
Test script to verify the fix for nested aesthetics issue.

This test script reproduces the specific case that was causing the TypeError:
"Expected a pandas DataFrame, got Aesthetics instead."
"""

from ggviews import ggplot, aes, load_dataset

# Load the mtcars dataset
mtcars = load_dataset("mtcars")

# The problematic pattern: using aes() as first positional argument to geom_*
# This was failing with: TypeError: Expected a pandas DataFrame, got Aesthetics instead
plot = ggplot(mtcars, aes(x="wt", y="mpg")).geom_point(aes(color="cyl"), size=5, alpha=0.7)

# Display the plot
print("Plot created successfully!")
