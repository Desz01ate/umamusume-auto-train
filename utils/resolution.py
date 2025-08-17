import pyautogui
from typing import Tuple, Optional

# Base resolution that all coordinates are designed for
BASE_RESOLUTION = (1920, 1080)

# Supported 16:9 resolutions
SUPPORTED_RESOLUTIONS = [
    (1280, 720),   # 720p
    (1366, 768),   # Common laptop
    (1600, 900),   # 900p
    (1920, 1080),  # 1080p (original)
    (2560, 1440),  # 1440p
    (3840, 2160),  # 4K
]

class ResolutionManager:
    def __init__(self):
        self.current_resolution = self.detect_resolution()
        self.scale_x, self.scale_y = self.calculate_scale_factors()
        
    def detect_resolution(self) -> Tuple[int, int]:
        """Detect current screen resolution"""
        size = pyautogui.size()
        return (size.width, size.height)
    
    def calculate_scale_factors(self) -> Tuple[float, float]:
        """Calculate scaling factors based on current resolution vs base resolution"""
        scale_x = self.current_resolution[0] / BASE_RESOLUTION[0]
        scale_y = self.current_resolution[1] / BASE_RESOLUTION[1]
        return scale_x, scale_y
    
    def is_supported_resolution(self) -> bool:
        """Check if current resolution is in supported list or has correct aspect ratio"""
        if self.current_resolution in SUPPORTED_RESOLUTIONS:
            return True
        
        # Check if aspect ratio is close to 16:9
        current_ratio = self.current_resolution[0] / self.current_resolution[1]
        target_ratio = 16 / 9
        return abs(current_ratio - target_ratio) < 0.1
    
    def scale_coordinate(self, x: int, y: int) -> Tuple[int, int]:
        """Scale a coordinate from base resolution to current resolution"""
        scaled_x = int(x * self.scale_x)
        scaled_y = int(y * self.scale_y)
        return scaled_x, scaled_y
    
    def scale_region(self, region: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
        """Scale a region (x, y, width, height) from base resolution to current resolution"""
        x, y, width, height = region
        scaled_x = int(x * self.scale_x)
        scaled_y = int(y * self.scale_y)
        scaled_width = int(width * self.scale_x)
        scaled_height = int(height * self.scale_y)
        return scaled_x, scaled_y, scaled_width, scaled_height
    
    def scale_relative_region(self, rel_region: Tuple[float, float, float, float]) -> Tuple[int, int, int, int]:
        """Convert relative coordinates (0.0-1.0) to absolute coordinates for current resolution"""
        rel_x, rel_y, rel_width, rel_height = rel_region
        x = int(rel_x * self.current_resolution[0])
        y = int(rel_y * self.current_resolution[1])
        width = int(rel_width * self.current_resolution[0])
        height = int(rel_height * self.current_resolution[1])
        return x, y, width, height
    
    def get_resolution_info(self) -> dict:
        """Get detailed resolution information"""
        return {
            "current_resolution": self.current_resolution,
            "base_resolution": BASE_RESOLUTION,
            "scale_factors": (self.scale_x, self.scale_y),
            "is_supported": self.is_supported_resolution(),
            "aspect_ratio": self.current_resolution[0] / self.current_resolution[1]
        }

# Global resolution manager instance
_resolution_manager = None

def get_resolution_manager() -> ResolutionManager:
    """Get the global resolution manager instance"""
    global _resolution_manager
    if _resolution_manager is None:
        _resolution_manager = ResolutionManager()
    return _resolution_manager

def reset_resolution_manager():
    """Reset the resolution manager (useful for testing or resolution changes)"""
    global _resolution_manager
    _resolution_manager = None

# Convenience functions
def scale_coordinate(x: int, y: int) -> Tuple[int, int]:
    """Scale a coordinate using the global resolution manager"""
    return get_resolution_manager().scale_coordinate(x, y)

def scale_region(region: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
    """Scale a region using the global resolution manager"""
    return get_resolution_manager().scale_region(region)

def scale_relative_region(rel_region: Tuple[float, float, float, float]) -> Tuple[int, int, int, int]:
    """Convert relative coordinates to absolute using the global resolution manager"""
    return get_resolution_manager().scale_relative_region(rel_region)

def get_current_resolution() -> Tuple[int, int]:
    """Get current screen resolution"""
    return get_resolution_manager().current_resolution

def is_supported_resolution() -> bool:
    """Check if current resolution is supported"""
    return get_resolution_manager().is_supported_resolution()