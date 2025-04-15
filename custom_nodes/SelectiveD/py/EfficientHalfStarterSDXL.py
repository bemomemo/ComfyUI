import nodes
from comfy_extras import nodes_clip_sdxl
from comfy_extras import nodes_freelunch

class EfficientHalfStarterSDXL:
    RESOLUTIONS = ["Cinematic (1536x640)", "Widescreen (1344x768)", "Photo (1216x832)", "Portrait (1152x896)", "Square (1024x1024)"]
    ASPECT = ["Vertical", "Horizontal"]

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "positive_prompt": ("STRING", {
                    "multiline": True,
                    "default": ""
                },),
                "negative_prompt": ("STRING", {
                    "multiline": True,
                    "default": ""
                },),
                "ckpt_model": ("MODEL",),
                "ckpt_clip": ("CLIP",),
                "ckpt_vae": ("VAE",),
                "stop_at_clip_layer": ("INT", {"default": 0, "min": -24, "max": 0, "step": 1},),
                "resolution": (EfficientHalfStarterSDXL.RESOLUTIONS, {"default": "Cinematic (1536x640)"},),
                "aspect": (EfficientHalfStarterSDXL.ASPECT, {"default": "Vertical"},),
                "resolution_multiply": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "step": 0.01,
                    "round": 0.01,
                    "display": "number"
                },),
                "target_multiply": ("FLOAT", {
                    "default": 1.5,
                    "min": 0.0,
                    "step": 0.01,
                    "round": 0.01,
                    "display": "number"
                },),
                "freeu_enable": (["enable", "disable"],),
                "b1": ("FLOAT", {
                    "default": 1.1,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.01,
                    "round": 0.01,
                    "display": "number"
                },),
                "b2": ("FLOAT", {
                    "default": 1.2,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.01,
                    "round": 0.01,
                    "display": "number"
                },),
                "s1": ("FLOAT", {
                    "default": 0.9,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.01,
                    "round": 0.01,
                    "display": "number"
                },),
                "s2": ("FLOAT", {
                    "default": 0.2,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.01,
                    "round": 0.01,
                    "display": "number"
                },),
            }
        }
    
    RETURN_TYPES = ("MODEL", "CLIP", "VAE", "CONDITIONING", "CONDITIONING", "LATENT", "STRING", "STRING",)
    RETURN_NAMES = ("model", "clip", "vae", "positive", "negative", "latent", "positive_prompt", "negative_prompt",)

    FUNCTION = "runStarter"

    CATEGORY = "SelectiveD"

    def runStarter(self, positive_prompt, negative_prompt, ckpt_model, ckpt_clip, ckpt_vae, stop_at_clip_layer, resolution, aspect, resolution_multiply, target_multiply, freeu_enable, b1, b2, s1, s2):
        match resolution:
            case "Cinematic (1536x640)":
                width_height = (1536, 640)
            case "Widescreen (1344x768)":
                width_height = (1344, 768)
            case "Photo (1216x832)":
                width_height = (1216, 832)
            case "Portrait (1152x896)":
                width_height = (1152, 896)
            case _:
                width_height = (1024, 1024)

        if aspect == "Vertical":
            width_height = tuple(reversed(width_height))

        if resolution_multiply != 1.0:
            width_height = (width_height[0] * resolution_multiply, width_height[1] * resolution_multiply)

        if target_multiply != 1.0:
            target_width_height = (width_height[0] * target_multiply, width_height[1] * target_multiply)

        clipEncodePositive = nodes_clip_sdxl.CLIPTextEncodeSDXL()
        clipEncodeNegative = nodes_clip_sdxl.CLIPTextEncodeSDXL()
        emptyLatent = nodes.EmptyLatentImage()
        #vaeEncode = nodes.VAEEncode()
        loadedClip = ckpt_clip

        if stop_at_clip_layer:
            loadedClip = loadedClip.clone()
            loadedClip.clip_layer(stop_at_clip_layer)

        positiveConditioning = clipEncodePositive.encode(loadedClip, width_height[0], width_height[1], 0, 0, target_width_height[0], target_width_height[1], positive_prompt, positive_prompt)
        negativeConditioning = clipEncodeNegative.encode(loadedClip, width_height[0], width_height[1], 0, 0, target_width_height[0], target_width_height[1], negative_prompt, negative_prompt)
        latent = emptyLatent.generate(width_height[0], width_height[1])

        if freeu_enable == "enable":
            freeuv2 = nodes_freelunch.FreeU_V2()
            ckpt_model = freeuv2.patch(ckpt_model, b1, b2, s1, s2)[0]

        return (ckpt_model, loadedClip, ckpt_vae) + positiveConditioning + negativeConditioning + latent + (positive_prompt, negative_prompt,)
    
NODE_CLASS_MAPPINGS = {
    "EfficientHalfStarterSDXL": EfficientHalfStarterSDXL
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EfficientHalfStarterSDXL": "Efficient Half Starter SDXL"
}
