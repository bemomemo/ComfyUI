class NormalizeDimensions:    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {
                    "default": 0,
                    "min": 1,
                    "max": 2048,
                    "step": 1,
                    "display": "number"
                }),
                "height": ("INT", {
                    "default": 0,
                    "min": 1,
                    "max": 2048,
                    "step": 1,
                    "display": "number"
                }),
                "scale_size": ("INT", {
                    "default": 0,
                    "min": 1,
                    "max": 2048,
                    "step": 1,
                    "display": "number"
                }),
            },
        }

    RETURN_TYPES = ("INT","INT",)
    RETURN_NAMES = ("scale_width","scale_height",)

    FUNCTION = "scale"

    #OUTPUT_NODE = False

    CATEGORY = "SelectiveD"

    def scale(self, width, height, scale_size):

        print(f"""normalize input:
                width = {width}
                height = {height}
            """)

        if width == height:
            print(f"""normalize:
                width and height = {round(scale_size)}
            """)
            return (round(scale_size),round(scale_size),)
        elif width > height:
            scale_height = (scale_size / width) * height

            print(f"""normalize:
                width = {round(scale_size)}
                height = {round(scale_height)}
            """)
            return (round(scale_size),round(scale_height),)
        else:
            scale_width = (scale_size / height) * width

            print(f"""normalize:
                width = {round(scale_width)}
                height = {round(scale_size)}
            """)
            return (round(scale_width),round(scale_size),)


NODE_CLASS_MAPPINGS = {
    "NormalizeDimensions": NormalizeDimensions
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "NormalizeDimensions": "Normalize Dimensions"
}
