# Sorting Algorithm Visualizer

A Python-based tool that visualizes common sorting algorithms with animated graphics and sound effects.

![Sorting Algorithm Visualization](https://github.com/NikolasRoufas/Visualised-Algorithms/blob/main/Figure_1.png)

## Overview

This project provides an educational tool to visualize how different sorting algorithms work in real-time. It uses matplotlib for visualization and pygame for sound effects, creating an interactive experience that helps users understand the mechanics of various sorting algorithms.

## Features

- **Interactive Visualization**: Watch algorithms sort data in real-time with color-coded bars
- **Audio Feedback**: Hear sound effects that correspond to comparisons and swaps
- **Algorithm Metrics**: Track the number of comparisons and swaps for each algorithm
- **Multiple Algorithms**: Currently supports:
  - Bubble Sort
  - Selection Sort
  - Insertion Sort
  - Merge Sort
  - Quick Sort
- **Customizable Parameters**: Adjust array size and animation speed

## Requirements

- Python 3.6+
- matplotlib
- numpy
- pygame

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/nikolaosroufas/Visualised-Algorithms
   cd Visualised-Algorithms
   ```

2. Install required packages:
   ```
   pip install matplotlib numpy pygame
   ```

## Usage

Run the main script to start the visualizer:

```python
python sorting_visualizer.py
```

### Customizing Visualization

You can modify parameters in the `main()` function:

```python
def main():
    # Customize array size and animation interval (milliseconds)
    visualizer = SortingVisualizer(array_size=50, interval=50)
    
    # Choose algorithm: "bubble", "selection", "insertion", "merge", or "quick"
    algorithm = "quick" 
    visualizer.animate(algorithm)
```

## How It Works

The visualizer represents each value in the array as a vertical bar. As the sorting algorithm runs:

- White bars: Unsorted elements
- Gray bars: Elements being compared
- Dark gray: Special elements (like pivots in Quick Sort)
- Light gray: Sorted elements

Sound effects provide additional feedback:
- Different pitches represent different values
- Distinct sounds for comparisons, swaps, and section completions

## Implementation Details

The project is built using object-oriented programming principles:

- `SortingVisualizer` class handles the visualization setup and algorithm implementations
- Each sorting algorithm has its own method that returns frames for animation
- Sound generation is handled through pygame's mixer
- Matplotlib's animation functionality displays the sorting process

## Contributing

Contributions are welcome! Here are some ways you can contribute:

- Add new sorting algorithms
- Improve visualization features
- Optimize existing algorithms
- Add more customization options
- Improve documentation

## License

[MIT License](LICENSE)

## Acknowledgements

- Inspired by various sorting algorithm visualizations
- Uses matplotlib for rendering and animation
- Uses pygame for sound generation

---

Created by [Nikolaos Roufas]
