class VAEDecodeTiledCustom:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "samples": ("LATENT", ),
                "vae": ("VAE", ),
                "tile_size_x": ("INT", {
                    "default": 2048,
                    "min": 1,
                    "max": 8096,
                    "step": 1,
                    "display": "number"
                }),
                "tile_size_y": ("INT", {
                    "default": 2048,
                    "min": 1,
                    "max": 8096,
                    "step": 1,
                    "display": "number"
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)

    FUNCTION = "decode"

    CATEGORY = "SelectiveD"

    def decode(self, vae, samples, tile_size_x, tile_size_y):
        return (vae.decode_tiled(samples["samples"], tile_x=tile_size_x // 8, tile_y=tile_size_y // 8, ), )
    
NODE_CLASS_MAPPINGS = {
    "VAEDecodeTiledCustom": VAEDecodeTiledCustom
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VAEDecodeTiledCustom": "VAE Decode Tiled Custom"
}
