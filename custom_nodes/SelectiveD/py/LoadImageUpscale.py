import os
import nodes
import folder_paths
from comfy_extras import nodes_upscale_model

class LoadImageUpscale:
    upscale_methods = ["nearest-exact", "bilinear", "area", "bicubic", "lanczos"]

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {
            "required": {
                "image": (sorted(files), {"image_upload": True},),
                "model_name": (folder_paths.get_filename_list("upscale_models"),),
                "upscale_method": (s.upscale_methods, {"default": "lanczos"},),
                "scale_by": ("FLOAT", {"default": 1.5, "min": 0.01, "max": 8.0, "step": 0.01},),
            },
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)

    FUNCTION = "loadUpscale"

    CATEGORY = "SelectiveD"

    def loadUpscale(self, image, model_name, upscale_method, scale_by):
        image_loader = nodes.LoadImage()
        loaded_image = image_loader.load_image(image)[0]
        
        return runSelectivedUpscale(loaded_image, model_name, upscale_method, scale_by)
    
class EfficientImageUpscale:
    upscale_methods = ["nearest-exact", "bilinear", "area", "bicubic", "lanczos"]

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {
            "required": {
                "image_in": ("IMAGE",),
                "model_name": (folder_paths.get_filename_list("upscale_models"), ),
                "upscale_method": (s.upscale_methods, {"default": "lanczos"},),
                "scale_by": ("FLOAT", {"default": 1.5, "min": 0.01, "max": 8.0, "step": 0.01}),
            },
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)

    FUNCTION = "loadUpscale"

    CATEGORY = "SelectiveD"

    def loadUpscale(self, image_in, model_name, upscale_method, scale_by):        
        return runSelectivedUpscale(image_in, model_name, upscale_method, scale_by)

def runSelectivedUpscale(loaded_image, model_name, upscale_method, scale_by):
    upscale_model_loader = nodes_upscale_model.UpscaleModelLoader()
    upscale_with_model = nodes_upscale_model.ImageUpscaleWithModel()
    image_scale = nodes.ImageScale()

    loaded_upscale_model = upscale_model_loader.load_model(model_name)[0]

    initial_image_size = loaded_image.size()
    final_image_width = int(initial_image_size[2] * scale_by)
    final_image_height = int(initial_image_size[1] * scale_by)

    upscaled_image = upscale_with_model.upscale(loaded_upscale_model, loaded_image)[0]

    return image_scale.upscale(upscaled_image, upscale_method, final_image_width, final_image_height, "disabled")
    
NODE_CLASS_MAPPINGS = {
    "LoadImageUpscale": LoadImageUpscale,
    "EfficientImageUpscale": EfficientImageUpscale
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadImageUpscale": "Load Image Upscale",
    "EfficientImageUpscale": "Efficient Image Upscale"
}