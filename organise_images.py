import os
import pandas as pd
import shutil

# Paths
labels_file = '/home/user65/sample/sample_labels.csv'
images_dir = '/home/user65/sample/images/'  # Adjust if necessary
output_dir = '/home/user65/sample_classes/'

# Load the labels CSV
labels_df = pd.read_csv(labels_file)

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Process each row in the dataframe
for index, row in labels_df.iterrows():
    img_filename = row['Image Index']  # Use 'Image Index' for the filename
    finding_labels = row['Finding Labels']  # Use 'Finding Labels' for the class

    # Split multiple labels by commas (if present)
    labels = finding_labels.split(', ')

    # Move the image to the corresponding label directory for each label
    for label in labels:
        # Create a directory for the label if it doesn't exist
        label_dir = os.path.join(output_dir, label)
        os.makedirs(label_dir, exist_ok=True)

        # Move the image to the corresponding label directory
        img_src = os.path.join(images_dir, img_filename)
        img_dest = os.path.join(label_dir, img_filename)

        if os.path.exists(img_src):  # Check if the image exists
            shutil.copy(img_src, img_dest)  # Copy the image
        else:
            print(f"Image not found: {img_src}")

# Zip the organized directory
shutil.make_archive(output_dir, 'zip', output_dir)

print(f"Images organized and zipped into: {output_dir}.zip")
