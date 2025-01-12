import pygame
import sys
from Constants import *
import numpy as np
import random 
class PointCollector:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Track Point Collector")
        self.clock = pygame.time.Clock()
        self.points = []
        self.current_track = 0
        self.font = pygame.font.Font(None, 36)
        self.min_point_distance = 40  # Minimum distance between points
        
    def load_current_track(self):
        """Load the current track and create mask from non-transparent pixels"""
        self.track = pygame.image.load(LEVELS[self.current_track]["track_image"]).convert_alpha()
        # Create mask from track (non-transparent pixels)
        self.track_mask = pygame.mask.from_surface(self.track)
        # Also load border to avoid placing points too close to edges
        self.border = pygame.image.load(LEVELS[self.current_track]["border_image"]).convert_alpha()
        self.border_mask = pygame.mask.from_surface(self.border)

    def is_valid_point(self, pos):
        """Check if point is valid (on track but not on border)"""
        x, y = int(pos[0]), int(pos[1])
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            return False
        
        # Point should be on track but not on border
        return self.track_mask.get_at((x, y)) and not self.border_mask.get_at((x, y))

    def is_point_far_enough(self, new_point):
        """Check if point is far enough from existing points"""
        for point in self.points:
            distance = np.sqrt((point[0] - new_point[0])**2 + (point[1] - new_point[1])**2)
            if distance < self.min_point_distance:
                return False
        return True

    def auto_collect_points(self, target_count=100):
        """Automatically collect well-distributed points on the track"""
        self.points = []
        grid_size = 20  # Size of grid cells to ensure better distribution
        
        for x in range(0, WIDTH, grid_size):
            for y in range(0, HEIGHT, grid_size):
                # Add some randomness within each grid cell
                test_x = x + random.randint(0, grid_size-1)
                test_y = y + random.randint(0, grid_size-1)
                
                if (len(self.points) < target_count and 
                    self.is_valid_point((test_x, test_y)) and 
                    self.is_point_far_enough((test_x, test_y))):
                    self.points.append((test_x, test_y))
        
        print(f"Collected {len(self.points)} points")

    def draw(self):
        # Draw track
        self.screen.blit(self.track, (0, 0))
        
        # Draw collected points
        for point in self.points:
            pygame.draw.circle(self.screen, (255, 215, 0), point, 3)  # Gold color
        
        # Draw UI text
        text = f"Track {self.current_track + 1} - Points: {len(self.points)}"
        text_surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 10))
        
        # Draw instructions
        instructions = [
            "Left Click: Add point",
            "Right Click: Remove closest point",
            "A: Auto-collect points",
            "S: Save points",
            "N: Next track",
            "P: Previous track",
            "C: Clear points",
            "Q: Quit"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_surface = self.font.render(instruction, True, (255, 255, 255))
            self.screen.blit(inst_surface, (10, 50 + i * 30))

    def save_points(self):
        """Save points in a format ready to paste into Constants.py"""
        track_name = f"track{self.current_track + 1}_points"
        points_str = f"{track_name} = [\n"
        for point in self.points:
            points_str += f"    {point},\n"
        points_str += "]\n"
        
        # Save to file and print to console
        with open(f"{track_name}.txt", "w") as f:
            f.write(points_str)
        
        print(f"\nSaved {len(self.points)} points for {track_name}")
        print("Copy this into Constants.py:")
        print(points_str)
    
    def run(self):
        self.load_current_track()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    pygame.quit()
                    return
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        if (self.is_valid_point(event.pos) and 
                            self.is_point_far_enough(event.pos)):
                            self.points.append(event.pos)
                    elif event.button == 3:  # Right click
                        if self.points:
                            idx = self.find_closest_point(event.pos)
                            if idx is not None:
                                self.points.pop(idx)
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:  # Save
                        self.save_points()
                    elif event.key == pygame.K_a:  # Auto-collect
                        self.auto_collect_points()
                    elif event.key == pygame.K_n:  # Next track
                        self.current_track = (self.current_track + 1) % len(LEVELS)
                        self.load_current_track()
                        self.points = []
                    elif event.key == pygame.K_p:  # Previous track
                        self.current_track = (self.current_track - 1) % len(LEVELS)
                        self.load_current_track()
                        self.points = []
                    elif event.key == pygame.K_c:  # Clear points
                        self.points = []
            
            self.screen.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    collector = PointCollector()
    collector.run()