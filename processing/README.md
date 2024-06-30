# Flow Field Visualization README

This repository contains four sketches for a flow field visualization in Processing: `visualizationGlobus`, `Flowfield`, `ParticleClass`, and `WaveExtractor`. Below is an explanation of each sketch and how the different variables affect the flow field.

## Table of Contents

- [Setup](#setup)
- [Sketch Descriptions](#sketch-descriptions)
  - [visualizationGlobus](#visualizationglobus)
  - [Flowfield](#flowfield)
  - [ParticleClass](#particleclass)
  - [WaveExtractor](#waveextractor)
- [Variables Explanation](#variables-explanation)

## Setup

To run the sketches, you need to have Processing installed on your machine. Clone this repository and open the `.pde` files in the Processing IDE.

```sh
git clone <repository_url>
```

## Sketch Descriptions

### visualizationGlobus

This is the main sketch that combines all the other components to create the flow field visualization.

#### Key Variables

- `noOfPoints`: Determines the number of particles in the visualization.
- `storyCounter`: Keeps track of the current story being played.
- `totalStories`: The total number of stories available.
- `col`: The color used for special particles, updated based on `storyCounter`.

### Flowfield

This class generates and updates the flow field grid, which influences the movement of particles.

#### Key Variables

- `inc`: Controls the smoothness of direction changes in the flow field.
- `scl`: The scale of the flow field grid.
- `zoff`: The z-offset for Perlin noise, affecting the evolution of the flow field over time.
- `cols`, `rows`: The number of columns and rows in the flow field grid.
- `flowField`: An array of PVector objects representing the flow vectors at each grid point.

#### Methods

- `update()`: Updates the flow field vectors based on Perlin noise.
- `lookup(PVector lookup)`: Returns the flow vector at a given position.

### ParticleClass

This class defines the particles that move according to the flow field vectors.

#### Key Variables

- `pos`, `vel`, `acc`: PVector objects representing the position, velocity, and acceleration of the particle.
- `maxSpeed`: The maximum speed of the particles.
- `col`: The color of the particles.

#### Methods

- `setColor(int col)`: Sets the color of the particle.
- `update()`: Updates the particle's position based on its velocity.
- `follow(PVector force)`: Applies a force to the particle, making it follow the flow field vectors.
- `show()`: Renders the particle on the screen.
- `edges()`: Wraps the particle around the edges of the screen.

### WaveExtractor

This class handles the extraction and analysis of audio data from `.wav` files, which influences the special flow field visualization.

#### Key Variables

- `minim`, `player`: Objects for handling audio playback and extraction.
- `leftBuffer`, `rightBuffer`: Buffers for left and right audio channels.
- `fft`: Fast Fourier Transform object for frequency analysis.
- `leftChannelData`, `rightChannelData`: Arrays for storing audio data of each channel.
- `frequencyData`: Array for storing frequency data.

#### Methods

- `update()`: Updates the audio and frequency data.
- `getLeftChannelData()`, `getRightChannelData()`, `getFrequencyData()`: Return the respective audio data arrays.
- `close()`: Closes the audio player and stops Minim.

## Variables Explanation

- **Grid Scale (`scl`)**: Determines the size of each cell in the flow field grid. Smaller values create more detailed flow fields.
- **Smoothness (`inc`)**: Controls how smoothly the direction changes in the flow field. Smaller values result in smoother transitions.
- **Z-Offset (`zoff`)**: Affects the speed at which the flow field evolves over time.
- **Max Speed (`maxSpeed`)**: Sets the maximum speed for particles. Higher values make particles move faster.
- **Color (`col`)**: Changes the color of particles in the special visualization. Updated based on the `storyCounter` to create dynamic visual effects.

This setup creates a dynamic and interactive visualization that reacts to both predefined flow field patterns and audio input, providing a unique and engaging experience.