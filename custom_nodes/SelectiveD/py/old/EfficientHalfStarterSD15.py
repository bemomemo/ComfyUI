import nodes
from comfy_extras import nodes_freelunch
from custom_nodes.ComfyUI_ADV_CLIP_emb import nodes as clip_nodes

class EfficientHalfStarterSD15:
    RESOLUTIONS = ["512x512", "640x512", "768x512", "768x432"]

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
                "token_normalization": (["none", "mean", "length", "length+mean"],),
                "weight_interpretation": (["comfy", "A1111", "compel", "comfy++" ,"down_weight"],),
                "ckpt_model": ("MODEL",),
                "ckpt_clip": ("CLIP",),
                "ckpt_vae": ("VAE",),
                "stop_at_clip_layer": ("INT", {"default": 0, "min": -24, "max": 0, "step": 1},),
                "resolution": (EfficientHalfStarterSD15.RESOLUTIONS, {"default": "768x432"},),
                "invert_resolution": (["enable", "disable"],),
                "resolution_multiply": ("FLOAT", {
                    "default": 1.0,
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

    def runStarter(self, positive_prompt, negative_prompt, token_normalization, weight_interpretation, ckpt_model, ckpt_clip, ckpt_vae, stop_at_clip_layer, resolution, invert_resolution, resolution_multiply, freeu_enable, b1, b2, s1, s2):
        match resolution:
            case "512x512":
                width_height = (512, 512)
            case "640x512":
                width_height = (640, 512)
            case "768x512":
                width_height = (768, 512)
            case _:
                width_height = (768, 432)

        if invert_resolution == "enable":
            width_height = tuple(reversed(width_height))

        if resolution_multiply != 1.0:
            width_height = (width_height[0] * resolution_multiply, width_height[1] * resolution_multiply)

        clipEncodePositive = clip_nodes.AdvancedCLIPTextEncode()
        clipEncodeNegative = clip_nodes.AdvancedCLIPTextEncode()
        emptyLatent = nodes.EmptyLatentImage()
        #vaeEncode = nodes.VAEEncode()

        loadedClip = ckpt_clip

        if stop_at_clip_layer:
            loadedClip = loadedClip.clone()
            loadedClip.clip_layer(stop_at_clip_layer)

        positiveConditioning = clipEncodePositive.encode(loadedClip, positive_prompt, token_normalization, weight_interpretation)
        negativeConditioning = clipEncodeNegative.encode(loadedClip, negative_prompt, token_normalization, weight_interpretation)
        latent = emptyLatent.generate(width_height[0], width_height[1])

        if freeu_enable == "enable":
            freeuv2 = nodes_freelunch.FreeU_V2()
            ckpt_model = freeuv2.patch(ckpt_model, b1, b2, s1, s2)[0]

        return (ckpt_model, loadedClip, ckpt_vae) + positiveConditioning + negativeConditioning + latent + (positive_prompt, negative_prompt,)
    
NODE_CLASS_MAPPINGS = {
    "EfficientHalfStarterSD15": EfficientHalfStarterSD15
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EfficientHalfStarterSD15": "Efficient Half Starter SD1.5"
}
