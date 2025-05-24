import torch
import torchvision.utils as vutils
import os
from model import Generator  # Import your generator model
import config  # Assuming you have a config file for constants like DEVICE, Z_DIM

# Create a directory to save the generated images
os.makedirs("generated_images_from_checkpoint", exist_ok=True)

# Function to load the generator from the 'generator.pth'
def load_generator_from_checkpoint(checkpoint_path):
    # Initialize the generator
    gen = Generator(config.Z_DIM, config.IN_CHANNELS, img_channels=config.CHANNELS_IMG).to(config.DEVICE)
    
    # Load the checkpoint
    print(f"Loading generator weights from {checkpoint_path}...")
    checkpoint = torch.load(checkpoint_path, map_location=config.DEVICE)
    
    # If the checkpoint contains additional info (e.g., "state_dict" key), extract only the state dict
    if "state_dict" in checkpoint:
        checkpoint = checkpoint["state_dict"]
    
    # Load the state dict into the generator
    gen.load_state_dict(checkpoint)
    
    return gen

# Function to generate and save images using the loaded generator
def generate_and_save_images(gen, num_images=32, step=6):  # Assuming step=6 for 1024x1024 images
    # Set generator to evaluation mode
    gen.eval()
    
    # Generate random noise
    noise = torch.randn(num_images, config.Z_DIM, 1, 1).to(config.DEVICE)
    
    # Alpha set to 1.0 (as training is complete) for fully blended images
    alpha = 1.0
    
    with torch.no_grad():
        fake_images = gen(noise, alpha, step) * 0.5 + 0.5  # Rescale to [0, 1]
    
    # Save the generated images
    file_path = "generated_images_from_checkpoint/generated_images.png"
    vutils.save_image(fake_images, file_path, normalize=True)
    print(f"Saved generated images to {file_path}")

def main():
    # Path to the generator weights ('generator.pth')
    checkpoint_gen_path = "/home/user65/progan/generator.pth"  # Update with the correct path if needed
    
    # Load the generator from the 'generator.pth' file
    generator = load_generator_from_checkpoint(checkpoint_gen_path)
    
    # Generate and save images
    generate_and_save_images(generator)

if __name__ == "__main__":
    main()
