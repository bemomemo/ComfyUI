class IntIncrement:
    def __init__(self):
        self.counters = {}

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 99999}),
            }
        }
    
    RETURN_TYPES = ("SEED", "INT", "STRING")
    RETURN_NAMES = ("seed", "integer", "padded")

    #OUTPUT_NODE = True

    #OUTPUT_IS_LIST = (True,)

    FUNCTION = "increment"

    CATEGORY = "SelectiveD"

    def increment(self, seed):
        return ({"seed": seed, }, int(seed), str(seed).zfill(5))
    
#WEB_DIRECTORY = "./selectived-web"

NODE_CLASS_MAPPINGS = {
    "IntIncrement": IntIncrement,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IntIncrement": "Int Increment",
}