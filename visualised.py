import matplotlib.pyplot as plt
import numpy as np
import random
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
import pygame

class SortingVisualizer:
    def __init__(self, array_size=50, interval=50):
        self.array_size = array_size
        self.interval = interval
        self.array = np.random.randint(1, 101, array_size)
        self.comparisons = 0
        self.swaps = 0
        
        pygame.mixer.init()
        self.setup_sounds()
        
        self.fig, self.ax = plt.subplots(figsize=(10, 6), facecolor='black')
        self.ax.set_xlim(0, array_size)
        self.ax.set_ylim(0, 110)
        self.ax.set_title("Sorting Algorithm Visualization", color='white')
        self.ax.set_xlabel("Index", color='white')
        self.ax.set_ylabel("Value", color='white')
        self.ax.set_facecolor('black')
        
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        for spine in self.ax.spines.values():
            spine.set_color('white')
        
        self.bar_rects = self.ax.bar(range(len(self.array)), self.array, align="edge", 
                                     color='white', edgecolor='gray', alpha=0.8)
        
        self.text = self.ax.text(0.02, 0.95, "", transform=self.ax.transAxes, color='white')
        
        self.default_color = 'white'
        self.comparison_color = '#777777'
        self.sorted_color = '#DDDDDD'
        self.colors = [self.default_color] * self.array_size
    
    def setup_sounds(self):
        self.sound_enabled = True
        try:
            self.create_sound_samples()
            
            self.swap_sound = self.generate_tone(440, 0.01)
            self.comparison_sound = self.generate_tone(330, 0.01)
            self.section_complete_sound = self.generate_tone(880, 0.05)
            self.sort_complete_sound = self.generate_tone(1320, 0.2)
        except:
            print("Sound initialization failed. Running without sound.")
            self.sound_enabled = False
    
    def create_sound_samples(self):
        self.value_sounds = {}
        for i in range(1, 101):
            freq = 220 + (i * 6.6)
            self.value_sounds[i] = self.generate_tone(freq, 0.01)
    
    def generate_tone(self, frequency, duration, volume=0.3):
        sample_rate = 44100
        
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        wave = np.sin(frequency * 2 * np.pi * t) * volume
        
        sound_array = (wave * 32767).astype(np.int16)
        
        sound = pygame.mixer.Sound(buffer=sound_array)
        return sound
    
    def play_value_sound(self, value):
        if self.sound_enabled:
            self.value_sounds[value].play()
    
    def play_swap_sound(self):
        if self.sound_enabled:
            self.swap_sound.play()
    
    def play_comparison_sound(self):
        if self.sound_enabled:
            self.comparison_sound.play()
    
    def play_section_complete_sound(self):
        if self.sound_enabled:
            self.section_complete_sound.play()
    
    def play_sort_complete_sound(self):
        if self.sound_enabled:
            self.sort_complete_sound.play()

    def update_plot(self, array, colors, comparisons, swaps):
        for rect, val, color in zip(self.bar_rects, array, colors):
            rect.set_height(val)
            rect.set_color(color)
        self.text.set_text(f"Comparisons: {comparisons}, Swaps: {swaps}")
        
    def bubble_sort(self):
        array = self.array.copy()
        colors = [self.default_color] * len(array)
        comparisons = 0
        swaps = 0
        
        frames = []
        
        frames.append((array.copy(), colors.copy(), comparisons, swaps, None))
        
        for i in range(len(array)):
            for j in range(0, len(array) - i - 1):
                colors[j] = self.comparison_color
                colors[j + 1] = self.comparison_color
                comparisons += 1
                
                frames.append((array.copy(), colors.copy(), comparisons, swaps, 
                              lambda: self.play_comparison_sound()))
                
                if array[j] > array[j + 1]:
                    array[j], array[j + 1] = array[j + 1], array[j]
                    swaps += 1
                    
                    frames.append((array.copy(), colors.copy(), comparisons, swaps,
                                  lambda val=array[j]: (self.play_swap_sound(), self.play_value_sound(val))))
                else:
                    frames.append((array.copy(), colors.copy(), comparisons, swaps,
                                  lambda val=array[j]: self.play_value_sound(val)))
                
                colors[j] = self.default_color
                colors[j + 1] = self.default_color
            
            colors[len(array) - i - 1] = self.sorted_color
            frames.append((array.copy(), colors.copy(), comparisons, swaps,
                           lambda: self.play_section_complete_sound()))
        
        colors = [self.sorted_color] * len(array)
        frames.append((array.copy(), colors.copy(), comparisons, swaps,
                       lambda: self.play_sort_complete_sound()))
        
        return frames
    
    def selection_sort(self):
        array = self.array.copy()
        colors = [self.default_color] * len(array)
        comparisons = 0
        swaps = 0
        
        frames = []
        
        frames.append((array.copy(), colors.copy(), comparisons, swaps, None))
        
        for i in range(len(array)):
            min_idx = i
            colors[i] = self.comparison_color
            frames.append((array.copy(), colors.copy(), comparisons, swaps, None))
            
            for j in range(i + 1, len(array)):
                colors[j] = self.comparison_color
                comparisons += 1
                frames.append((array.copy(), colors.copy(), comparisons, swaps,
                              lambda: self.play_comparison_sound()))
                
                if array[j] < array[min_idx]:
                    if min_idx != i:
                        colors[min_idx] = self.default_color
                    min_idx = j
                    colors[min_idx] = '#AAAAAA'
                    frames.append((array.copy(), colors.copy(), comparisons, swaps,
                                  lambda val=array[j]: self.play_value_sound(val)))
                else:
                    colors[j] = self.default_color
            
            if min_idx != i:
                array[i], array[min_idx] = array[min_idx], array[i]
                swaps += 1
                colors[min_idx] = self.default_color
                frames.append((array.copy(), colors.copy(), comparisons, swaps,
                              lambda: self.play_swap_sound()))
            
            colors[i] = self.sorted_color
            frames.append((array.copy(), colors.copy(), comparisons, swaps,
                          lambda: self.play_section_complete_sound()))
        
        frames.append((array.copy(), colors.copy(), comparisons, swaps,
                      lambda: self.play_sort_complete_sound()))
        
        return frames
    
    def insertion_sort(self):
        array = self.array.copy()
        colors = [self.default_color] * len(array)
        comparisons = 0
        swaps = 0
        
        frames = []
        
        frames.append((array.copy(), colors.copy(), comparisons, swaps, None))
        
        colors[0] = self.sorted_color
        frames.append((array.copy(), colors.copy(), comparisons, swaps, None))
        
        for i in range(1, len(array)):
            key = array[i]
            j = i - 1
            
            colors[i] = self.comparison_color
            frames.append((array.copy(), colors.copy(), comparisons, swaps,
                          lambda val=key: self.play_value_sound(val)))
            
            while j >= 0 and array[j] > key:
                comparisons += 1
                colors[j] = self.comparison_color
                frames.append((array.copy(), colors.copy(), comparisons, swaps,
                              lambda: self.play_comparison_sound()))
                
                array[j + 1] = array[j]
                swaps += 1
                frames.append((array.copy(), colors.copy(), comparisons, swaps,
                              lambda: self.play_swap_sound()))
                
                colors[j] = self.sorted_color
                j -= 1
            
            array[j + 1] = key
            
            colors[j + 1] = self.sorted_color
            frames.append((array.copy(), colors.copy(), comparisons, swaps,
                          lambda: self.play_section_complete_sound()))
        
        frames.append((array.copy(), colors.copy(), comparisons, swaps,
                      lambda: self.play_sort_complete_sound()))
        
        return frames
    
    def merge_sort(self):
        array = self.array.copy()
        colors = [self.default_color] * len(array)
        comparisons = 0
        swaps = 0
        
        frames = []
        
        frames.append((array.copy(), colors.copy(), comparisons, swaps, None))
        
        def merge(arr, left, mid, right):
            nonlocal comparisons, swaps, frames
            
            for i in range(left, right + 1):
                colors[i] = self.comparison_color
            frames.append((array.copy(), colors.copy(), comparisons, swaps, None))
            
            L = arr[left:mid + 1]
            R = arr[mid + 1:right + 1]
            
            i = j = 0
            k = left
            
            while i < len(L) and j < len(R):
                comparisons += 1
                frames.append((array.copy(), colors.copy(), comparisons, swaps,
                              lambda: self.play_comparison_sound()))
                
                if L[i] <= R[j]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                swaps += 1
                
                colors[k] = '#AAAAAA'
                frames.append((array.copy(), colors.copy(), comparisons, swaps,
                              lambda val=arr[k]: (self.play_swap_sound(), self.play_value_sound(val))))
                colors[k] = self.default_color
                k += 1
            
            while i < len(L):
                arr[k] = L[i]
                swaps += 1
                colors[k] = '#AAAAAA'
                frames.append((array.copy(), colors.copy(), comparisons, swaps,
                              lambda val=arr[k]: self.play_value_sound(val)))
                colors[k] = self.default_color
                i += 1
                k += 1
            
            while j < len(R):
                arr[k] = R[j]
                swaps += 1
                colors[k] = '#AAAAAA'
                frames.append((array.copy(), colors.copy(), comparisons, swaps,
                              lambda val=arr[k]: self.play_value_sound(val)))
                colors[k] = self.default_color
                j += 1
                k += 1
            
            for i in range(left, right + 1):
                colors[i] = self.default_color
            frames.append((array.copy(), colors.copy(), comparisons, swaps,
                          lambda: self.play_section_complete_sound()))
        
        def merge_sort_recursive(arr, left, right):
            if left < right:
                mid = (left + right) // 2
                
                for i in range(left, right + 1):
                    colors[i] = self.comparison_color
                frames.append((array.copy(), colors.copy(), comparisons, swaps, None))
                
                for i in range(left, right + 1):
                    colors[i] = self.default_color
                
                merge_sort_recursive(arr, left, mid)
                merge_sort_recursive(arr, mid + 1, right)
                
                merge(arr, left, mid, right)
        
        merge_sort_recursive(array, 0, len(array) - 1)
        
        colors = [self.sorted_color] * len(array)
        frames.append((array.copy(), colors.copy(), comparisons, swaps,
                      lambda: self.play_sort_complete_sound()))
        
        return frames
    
    def quick_sort(self):
        array = self.array.copy()
        colors = [self.default_color] * len(array)
        comparisons = 0
        swaps = 0
        
        frames = []
        
        frames.append((array.copy(), colors.copy(), comparisons, swaps, None))
        
        def partition(arr, low, high):
            nonlocal comparisons, swaps, frames
            
            pivot = arr[high]
            
            colors[high] = '#444444'
            frames.append((array.copy(), colors.copy(), comparisons, swaps,
                          lambda val=pivot: self.play_value_sound(val)))
            
            i = low - 1
            
            for j in range(low, high):
                colors[j] = self.comparison_color
                frames.append((array.copy(), colors.copy(), comparisons, swaps, None))
                
                comparisons += 1
                frames.append((array.copy(), colors.copy(), comparisons, swaps,
                              lambda: self.play_comparison_sound()))
                
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    swaps += 1
                    
                    colors[i] = '#AAAAAA'
                    frames.append((array.copy(), colors.copy(), comparisons, swaps,
                                  lambda val=arr[i]: (self.play_swap_sound(), self.play_value_sound(val))))
                
                colors[j] = self.default_color
                if i >= low:
                    colors[i] = self.default_color
            
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            swaps += 1
            
            colors[i + 1] = self.sorted_color
            frames.append((array.copy(), colors.copy(), comparisons, swaps,
                          lambda val=arr[i+1]: (self.play_swap_sound(), self.play_value_sound(val))))
            
            return i + 1
        
        def quick_sort_recursive(arr, low, high):
            if low < high:
                for i in range(low, high + 1):
                    colors[i] = '#EEEEEE'
                frames.append((array.copy(), colors.copy(), comparisons, swaps, None))
                
                for i in range(low, high + 1):
                    colors[i] = self.default_color
                
                pi = partition(arr, low, high)
                
                quick_sort_recursive(arr, low, pi - 1)
                quick_sort_recursive(arr, pi + 1, high)
        
        quick_sort_recursive(array, 0, len(array) - 1)
        
        colors = [self.sorted_color] * len(array)
        frames.append((array.copy(), colors.copy(), comparisons, swaps,
                      lambda: self.play_sort_complete_sound()))
        
        return frames
    
    def animate(self, sorting_algorithm):
        if sorting_algorithm == "bubble":
            frames = self.bubble_sort()
        elif sorting_algorithm == "selection":
            frames = self.selection_sort()
        elif sorting_algorithm == "insertion":
            frames = self.insertion_sort()
        elif sorting_algorithm == "merge":
            frames = self.merge_sort()
        elif sorting_algorithm == "quick":
            frames = self.quick_sort()
        else:
            raise ValueError("Unknown sorting algorithm")
        
        def update(frame_data):
            array, colors, comparisons, swaps, sound_func = frame_data
            self.update_plot(array, colors, comparisons, swaps)
            
            if sound_func:
                sound_func()
                
            return self.bar_rects
        
        anim = animation.FuncAnimation(
            self.fig, update, frames=frames, interval=self.interval, 
            blit=False, repeat=False
        )
        
        plt.tight_layout()
        plt.show()
        
        return anim

def main():
    visualizer = SortingVisualizer(array_size=200, interval=20)
    
    algorithm = "quick" #Change THis to whatever algo you want
    visualizer.animate(algorithm)

if __name__ == "__main__":
    main()
