class ImageInfo:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_in": ("IMAGE", {}),
            },
        }
    
    RETURN_TYPES = ("IMAGE","INT", "INT",)
    RETURN_NAMES = ("image","width","height",)

    OUTPUT_NODE = True

    #OUTPUT_IS_LIST = (True,)

    FUNCTION = "get_image_info"

    CATEGORY = "SelectiveD"

    def get_image_info(self, image_in):
        width = image_in.size()[2]
        height = image_in.size()[1]

        text = "Image Info:" + "\nwidth = " + str(image_in.size()[2]) + "\nheight = " + str(image_in.size()[1])

        #return ("ui": {"text": (value,)}, image_in.size()[2], image_in.size()[1],)
        return {"ui": {"text": text}, "result": (image_in, width, height)}
    
WEB_DIRECTORY = "./selectived-web"

NODE_CLASS_MAPPINGS = {
    "ImageInfo": ImageInfo,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageInfo": "Image Info",
}